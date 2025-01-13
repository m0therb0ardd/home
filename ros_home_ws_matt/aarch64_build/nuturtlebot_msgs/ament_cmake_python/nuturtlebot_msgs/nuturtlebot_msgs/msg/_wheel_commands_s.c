// generated from rosidl_generator_py/resource/_idl_support.c.em
// with input from nuturtlebot_msgs:msg/WheelCommands.idl
// generated code does not contain a copyright notice
#define NPY_NO_DEPRECATED_API NPY_1_7_API_VERSION
#include <Python.h>
#include <stdbool.h>
#ifndef _WIN32
# pragma GCC diagnostic push
# pragma GCC diagnostic ignored "-Wunused-function"
#endif
#include "numpy/ndarrayobject.h"
#ifndef _WIN32
# pragma GCC diagnostic pop
#endif
#include "rosidl_runtime_c/visibility_control.h"
#include "nuturtlebot_msgs/msg/detail/wheel_commands__struct.h"
#include "nuturtlebot_msgs/msg/detail/wheel_commands__functions.h"


ROSIDL_GENERATOR_C_EXPORT
bool nuturtlebot_msgs__msg__wheel_commands__convert_from_py(PyObject * _pymsg, void * _ros_message)
{
  // check that the passed message is of the expected Python class
  {
    char full_classname_dest[51];
    {
      char * class_name = NULL;
      char * module_name = NULL;
      {
        PyObject * class_attr = PyObject_GetAttrString(_pymsg, "__class__");
        if (class_attr) {
          PyObject * name_attr = PyObject_GetAttrString(class_attr, "__name__");
          if (name_attr) {
            class_name = (char *)PyUnicode_1BYTE_DATA(name_attr);
            Py_DECREF(name_attr);
          }
          PyObject * module_attr = PyObject_GetAttrString(class_attr, "__module__");
          if (module_attr) {
            module_name = (char *)PyUnicode_1BYTE_DATA(module_attr);
            Py_DECREF(module_attr);
          }
          Py_DECREF(class_attr);
        }
      }
      if (!class_name || !module_name) {
        return false;
      }
      snprintf(full_classname_dest, sizeof(full_classname_dest), "%s.%s", module_name, class_name);
    }
    assert(strncmp("nuturtlebot_msgs.msg._wheel_commands.WheelCommands", full_classname_dest, 50) == 0);
  }
  nuturtlebot_msgs__msg__WheelCommands * ros_message = _ros_message;
  {  // left_velocity
    PyObject * field = PyObject_GetAttrString(_pymsg, "left_velocity");
    if (!field) {
      return false;
    }
    assert(PyLong_Check(field));
    ros_message->left_velocity = (int32_t)PyLong_AsLong(field);
    Py_DECREF(field);
  }
  {  // right_velocity
    PyObject * field = PyObject_GetAttrString(_pymsg, "right_velocity");
    if (!field) {
      return false;
    }
    assert(PyLong_Check(field));
    ros_message->right_velocity = (int32_t)PyLong_AsLong(field);
    Py_DECREF(field);
  }

  return true;
}

ROSIDL_GENERATOR_C_EXPORT
PyObject * nuturtlebot_msgs__msg__wheel_commands__convert_to_py(void * raw_ros_message)
{
  /* NOTE(esteve): Call constructor of WheelCommands */
  PyObject * _pymessage = NULL;
  {
    PyObject * pymessage_module = PyImport_ImportModule("nuturtlebot_msgs.msg._wheel_commands");
    assert(pymessage_module);
    PyObject * pymessage_class = PyObject_GetAttrString(pymessage_module, "WheelCommands");
    assert(pymessage_class);
    Py_DECREF(pymessage_module);
    _pymessage = PyObject_CallObject(pymessage_class, NULL);
    Py_DECREF(pymessage_class);
    if (!_pymessage) {
      return NULL;
    }
  }
  nuturtlebot_msgs__msg__WheelCommands * ros_message = (nuturtlebot_msgs__msg__WheelCommands *)raw_ros_message;
  {  // left_velocity
    PyObject * field = NULL;
    field = PyLong_FromLong(ros_message->left_velocity);
    {
      int rc = PyObject_SetAttrString(_pymessage, "left_velocity", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // right_velocity
    PyObject * field = NULL;
    field = PyLong_FromLong(ros_message->right_velocity);
    {
      int rc = PyObject_SetAttrString(_pymessage, "right_velocity", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }

  // ownership of _pymessage is transferred to the caller
  return _pymessage;
}
