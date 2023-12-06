#define PY_SSIZE_T_CLEAN
#include <Python.h>

#define IMMORTAL_REFCNT UINT32_MAX


static PyObject* immortalize(PyObject *self, PyObject *args) {
  PyObject *ob;

  if (!PyArg_ParseTuple(args, "O", &ob))
      return NULL;

  if (ob->ob_refcnt == IMMORTAL_REFCNT)
    return Py_BuildValue("i", 0);

  Py_SET_REFCNT(ob, IMMORTAL_REFCNT);
  return Py_BuildValue("i", 1);
}

static PyObject* is_immortal(PyObject *self, PyObject *args) {
  PyObject *ob;

  if (!PyArg_ParseTuple(args, "O", &ob))
      return NULL;

  if (ob->ob_refcnt == IMMORTAL_REFCNT)
      Py_RETURN_TRUE;
  else
      Py_RETURN_FALSE;
}

static PyMethodDef MyMethods[] = {
  { "immortalize", immortalize, METH_VARARGS, "Immortalize an arbitrary object" },
  { "is_immortal", is_immortal, METH_VARARGS, "Check if an object is immortal"},
  { NULL, NULL, 0, NULL },
};


static struct PyModuleDef mymodule = {
  PyModuleDef_HEAD_INIT,
  "mymodule",
  NULL,
  -1,

  MyMethods,
};


PyMODINIT_FUNC PyInit_mymodule(void) {
    return PyModule_Create(&mymodule);
}
