#include <Python.h>

static PyObject *
ussp_call(PyObject *self, PyObject *args)
{
  const char *addr, *path, *remote;
  int timeout, ret;

  if (!PyArg_ParseTuple(args, "sssi", &addr, &path, &remote, &timeout))
    return NULL;
  ret = obex_push_python(addr, path, remote, timeout);
  return Py_BuildValue("i", ret);
}

static PyMethodDef pythonusspMethods[] = {
  {"ussp_call", ussp_call, METH_VARARGS, "Carry out the obex-send."},
  {NULL, NULL, 0, NULL}
};

PyMODINIT_FUNC
initpythonussp(void)
{
  (void) Py_InitModule("pythonussp", pythonusspMethods);
}
