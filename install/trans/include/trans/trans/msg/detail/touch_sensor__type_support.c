// generated from rosidl_typesupport_introspection_c/resource/idl__type_support.c.em
// with input from trans:msg/TouchSensor.idl
// generated code does not contain a copyright notice

#include <stddef.h>
#include "trans/msg/detail/touch_sensor__rosidl_typesupport_introspection_c.h"
#include "trans/msg/rosidl_typesupport_introspection_c__visibility_control.h"
#include "rosidl_typesupport_introspection_c/field_types.h"
#include "rosidl_typesupport_introspection_c/identifier.h"
#include "rosidl_typesupport_introspection_c/message_introspection.h"
#include "trans/msg/detail/touch_sensor__functions.h"
#include "trans/msg/detail/touch_sensor__struct.h"


// Include directives for member types
// Member `header`
#include "std_msgs/msg/header.h"
// Member `header`
#include "std_msgs/msg/detail/header__rosidl_typesupport_introspection_c.h"
// Member `names`
#include "rosidl_runtime_c/string_functions.h"
// Member `value`
#include "rosidl_runtime_c/primitives_sequence_functions.h"

#ifdef __cplusplus
extern "C"
{
#endif

void trans__msg__TouchSensor__rosidl_typesupport_introspection_c__TouchSensor_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  trans__msg__TouchSensor__init(message_memory);
}

void trans__msg__TouchSensor__rosidl_typesupport_introspection_c__TouchSensor_fini_function(void * message_memory)
{
  trans__msg__TouchSensor__fini(message_memory);
}

size_t trans__msg__TouchSensor__rosidl_typesupport_introspection_c__size_function__TouchSensor__names(
  const void * untyped_member)
{
  const rosidl_runtime_c__String__Sequence * member =
    (const rosidl_runtime_c__String__Sequence *)(untyped_member);
  return member->size;
}

const void * trans__msg__TouchSensor__rosidl_typesupport_introspection_c__get_const_function__TouchSensor__names(
  const void * untyped_member, size_t index)
{
  const rosidl_runtime_c__String__Sequence * member =
    (const rosidl_runtime_c__String__Sequence *)(untyped_member);
  return &member->data[index];
}

void * trans__msg__TouchSensor__rosidl_typesupport_introspection_c__get_function__TouchSensor__names(
  void * untyped_member, size_t index)
{
  rosidl_runtime_c__String__Sequence * member =
    (rosidl_runtime_c__String__Sequence *)(untyped_member);
  return &member->data[index];
}

void trans__msg__TouchSensor__rosidl_typesupport_introspection_c__fetch_function__TouchSensor__names(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const rosidl_runtime_c__String * item =
    ((const rosidl_runtime_c__String *)
    trans__msg__TouchSensor__rosidl_typesupport_introspection_c__get_const_function__TouchSensor__names(untyped_member, index));
  rosidl_runtime_c__String * value =
    (rosidl_runtime_c__String *)(untyped_value);
  *value = *item;
}

void trans__msg__TouchSensor__rosidl_typesupport_introspection_c__assign_function__TouchSensor__names(
  void * untyped_member, size_t index, const void * untyped_value)
{
  rosidl_runtime_c__String * item =
    ((rosidl_runtime_c__String *)
    trans__msg__TouchSensor__rosidl_typesupport_introspection_c__get_function__TouchSensor__names(untyped_member, index));
  const rosidl_runtime_c__String * value =
    (const rosidl_runtime_c__String *)(untyped_value);
  *item = *value;
}

bool trans__msg__TouchSensor__rosidl_typesupport_introspection_c__resize_function__TouchSensor__names(
  void * untyped_member, size_t size)
{
  rosidl_runtime_c__String__Sequence * member =
    (rosidl_runtime_c__String__Sequence *)(untyped_member);
  rosidl_runtime_c__String__Sequence__fini(member);
  return rosidl_runtime_c__String__Sequence__init(member, size);
}

size_t trans__msg__TouchSensor__rosidl_typesupport_introspection_c__size_function__TouchSensor__value(
  const void * untyped_member)
{
  const rosidl_runtime_c__float__Sequence * member =
    (const rosidl_runtime_c__float__Sequence *)(untyped_member);
  return member->size;
}

const void * trans__msg__TouchSensor__rosidl_typesupport_introspection_c__get_const_function__TouchSensor__value(
  const void * untyped_member, size_t index)
{
  const rosidl_runtime_c__float__Sequence * member =
    (const rosidl_runtime_c__float__Sequence *)(untyped_member);
  return &member->data[index];
}

void * trans__msg__TouchSensor__rosidl_typesupport_introspection_c__get_function__TouchSensor__value(
  void * untyped_member, size_t index)
{
  rosidl_runtime_c__float__Sequence * member =
    (rosidl_runtime_c__float__Sequence *)(untyped_member);
  return &member->data[index];
}

void trans__msg__TouchSensor__rosidl_typesupport_introspection_c__fetch_function__TouchSensor__value(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const float * item =
    ((const float *)
    trans__msg__TouchSensor__rosidl_typesupport_introspection_c__get_const_function__TouchSensor__value(untyped_member, index));
  float * value =
    (float *)(untyped_value);
  *value = *item;
}

void trans__msg__TouchSensor__rosidl_typesupport_introspection_c__assign_function__TouchSensor__value(
  void * untyped_member, size_t index, const void * untyped_value)
{
  float * item =
    ((float *)
    trans__msg__TouchSensor__rosidl_typesupport_introspection_c__get_function__TouchSensor__value(untyped_member, index));
  const float * value =
    (const float *)(untyped_value);
  *item = *value;
}

bool trans__msg__TouchSensor__rosidl_typesupport_introspection_c__resize_function__TouchSensor__value(
  void * untyped_member, size_t size)
{
  rosidl_runtime_c__float__Sequence * member =
    (rosidl_runtime_c__float__Sequence *)(untyped_member);
  rosidl_runtime_c__float__Sequence__fini(member);
  return rosidl_runtime_c__float__Sequence__init(member, size);
}

static rosidl_typesupport_introspection_c__MessageMember trans__msg__TouchSensor__rosidl_typesupport_introspection_c__TouchSensor_message_member_array[3] = {
  {
    "header",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message (initialized later)
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(trans__msg__TouchSensor, header),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "names",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_STRING,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    true,  // is array
    10,  // array size
    true,  // is upper bound
    offsetof(trans__msg__TouchSensor, names),  // bytes offset in struct
    NULL,  // default value
    trans__msg__TouchSensor__rosidl_typesupport_introspection_c__size_function__TouchSensor__names,  // size() function pointer
    trans__msg__TouchSensor__rosidl_typesupport_introspection_c__get_const_function__TouchSensor__names,  // get_const(index) function pointer
    trans__msg__TouchSensor__rosidl_typesupport_introspection_c__get_function__TouchSensor__names,  // get(index) function pointer
    trans__msg__TouchSensor__rosidl_typesupport_introspection_c__fetch_function__TouchSensor__names,  // fetch(index, &value) function pointer
    trans__msg__TouchSensor__rosidl_typesupport_introspection_c__assign_function__TouchSensor__names,  // assign(index, value) function pointer
    trans__msg__TouchSensor__rosidl_typesupport_introspection_c__resize_function__TouchSensor__names  // resize(index) function pointer
  },
  {
    "value",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_FLOAT,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    true,  // is array
    10,  // array size
    true,  // is upper bound
    offsetof(trans__msg__TouchSensor, value),  // bytes offset in struct
    NULL,  // default value
    trans__msg__TouchSensor__rosidl_typesupport_introspection_c__size_function__TouchSensor__value,  // size() function pointer
    trans__msg__TouchSensor__rosidl_typesupport_introspection_c__get_const_function__TouchSensor__value,  // get_const(index) function pointer
    trans__msg__TouchSensor__rosidl_typesupport_introspection_c__get_function__TouchSensor__value,  // get(index) function pointer
    trans__msg__TouchSensor__rosidl_typesupport_introspection_c__fetch_function__TouchSensor__value,  // fetch(index, &value) function pointer
    trans__msg__TouchSensor__rosidl_typesupport_introspection_c__assign_function__TouchSensor__value,  // assign(index, value) function pointer
    trans__msg__TouchSensor__rosidl_typesupport_introspection_c__resize_function__TouchSensor__value  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers trans__msg__TouchSensor__rosidl_typesupport_introspection_c__TouchSensor_message_members = {
  "trans__msg",  // message namespace
  "TouchSensor",  // message name
  3,  // number of fields
  sizeof(trans__msg__TouchSensor),
  trans__msg__TouchSensor__rosidl_typesupport_introspection_c__TouchSensor_message_member_array,  // message members
  trans__msg__TouchSensor__rosidl_typesupport_introspection_c__TouchSensor_init_function,  // function to initialize message memory (memory has to be allocated)
  trans__msg__TouchSensor__rosidl_typesupport_introspection_c__TouchSensor_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t trans__msg__TouchSensor__rosidl_typesupport_introspection_c__TouchSensor_message_type_support_handle = {
  0,
  &trans__msg__TouchSensor__rosidl_typesupport_introspection_c__TouchSensor_message_members,
  get_message_typesupport_handle_function,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_trans
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, trans, msg, TouchSensor)() {
  trans__msg__TouchSensor__rosidl_typesupport_introspection_c__TouchSensor_message_member_array[0].members_ =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, std_msgs, msg, Header)();
  if (!trans__msg__TouchSensor__rosidl_typesupport_introspection_c__TouchSensor_message_type_support_handle.typesupport_identifier) {
    trans__msg__TouchSensor__rosidl_typesupport_introspection_c__TouchSensor_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &trans__msg__TouchSensor__rosidl_typesupport_introspection_c__TouchSensor_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif
