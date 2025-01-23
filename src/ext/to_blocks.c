#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <numpy/arrayobject.h>

static PyObject* to_blocks(PyObject* self, PyObject* args) {
    PyArrayObject *pixels;
    int x0, y0, width, height;
    int invert;

    if (!PyArg_ParseTuple(args, "O!iiiip", &PyArray_Type, &pixels, &x0, &y0, &width, &height, &invert)) {
        return NULL;
    }

    if (PyArray_NDIM(pixels) != 2 || PyArray_TYPE(pixels) != NPY_UINT8) {
        PyErr_SetString(PyExc_ValueError, "pixels must be a 2D NumPy array of uint8");
        return NULL;
    }

    npy_intp pixels_height = PyArray_DIM(pixels, 0);
    npy_intp pixels_width = PyArray_DIM(pixels, 1);

    npy_intp output_rows = (height + 3) / 4;
    npy_intp output_cols = (width + 1) / 2;

    unsigned char* output = (unsigned char*)malloc(output_rows * output_cols);
    if (!output) {
        PyErr_SetString(PyExc_MemoryError, "Failed to allocate output array");
        return NULL;
    }

    unsigned char compare_value = invert ? 0 : 255;

    for (npy_intp row_block = 0; row_block < output_rows; ++row_block) {
        for (npy_intp col_block = 0; col_block < output_cols; ++col_block) {
            unsigned char block_value = 0;

            for (int dy = 0; dy < 4; ++dy) {
                for (int dx = 0; dx < 2; ++dx) {
                    int x = x0 + col_block * 2 + dx;
                    int y = y0 + row_block * 4 + dy;

                    if (x < pixels_width && y < pixels_height) {
                        unsigned char pixel_value = *(unsigned char*)PyArray_GETPTR2(pixels, y, x);
                        if (pixel_value == compare_value) {
                            block_value |= (1 << (dy * 2 + dx));
                        }
                    }
                }
            }

            output[row_block * output_cols + col_block] = block_value;
        }
    }

    // Create NumPy array from the native C array
    npy_intp dims[2] = {output_rows, output_cols};
    PyObject* result = PyArray_SimpleNewFromData(2, dims, NPY_UINT8, output);

    if (!result) {
        free(output);
        PyErr_SetString(PyExc_MemoryError, "Failed to create NumPy array from output data");
        return NULL;
    }

    PyArray_ENABLEFLAGS((PyArrayObject*)result, NPY_ARRAY_OWNDATA);

    return result;
}


static PyMethodDef methods[] = {
    {"to_blocks", (PyCFunction)to_blocks, METH_VARARGS, "Convert pixels array into 2x4 blocks."},
    {NULL, NULL, 0, NULL}
};

static struct PyModuleDef module = {
    PyModuleDef_HEAD_INIT,
    "convert",
    "A module to convert a pixel array into 2x4 blocks.",
    -1,
    methods
};

PyMODINIT_FUNC PyInit_convert(void) {
    import_array(); // Initialize NumPy C API
    return PyModule_Create(&module);
}
