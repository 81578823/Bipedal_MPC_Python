// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from trans:msg/TouchSensor.idl
// generated code does not contain a copyright notice

#ifndef TRANS__MSG__DETAIL__TOUCH_SENSOR__STRUCT_H_
#define TRANS__MSG__DETAIL__TOUCH_SENSOR__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

// Include directives for member types
// Member 'header'
#include "std_msgs/msg/detail/header__struct.h"
// Member 'names'
#include "rosidl_runtime_c/string.h"
// Member 'value'
#include "rosidl_runtime_c/primitives_sequence.h"

// constants for array fields with an upper bound
// names
enum
{
  trans__msg__TouchSensor__names__MAX_SIZE = 10
};
// value
enum
{
  trans__msg__TouchSensor__value__MAX_SIZE = 10
};

/// Struct defined in msg/TouchSensor in the package trans.
typedef struct trans__msg__TouchSensor
{
  std_msgs__msg__Header header;
  rosidl_runtime_c__String__Sequence names;
  rosidl_runtime_c__float__Sequence value;
} trans__msg__TouchSensor;

// Struct for a sequence of trans__msg__TouchSensor.
typedef struct trans__msg__TouchSensor__Sequence
{
  trans__msg__TouchSensor * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} trans__msg__TouchSensor__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // TRANS__MSG__DETAIL__TOUCH_SENSOR__STRUCT_H_
