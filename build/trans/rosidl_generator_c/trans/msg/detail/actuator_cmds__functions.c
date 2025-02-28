// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from trans:msg/ActuatorCmds.idl
// generated code does not contain a copyright notice
#include "trans/msg/detail/actuator_cmds__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"


// Include directives for member types
// Member `header`
#include "std_msgs/msg/detail/header__functions.h"
// Member `names`
#include "rosidl_runtime_c/string_functions.h"
// Member `gain_p`
// Member `pos_des`
// Member `gaid_d`
// Member `vel_des`
// Member `feedforward_torque`
#include "rosidl_runtime_c/primitives_sequence_functions.h"

bool
trans__msg__ActuatorCmds__init(trans__msg__ActuatorCmds * msg)
{
  if (!msg) {
    return false;
  }
  // header
  if (!std_msgs__msg__Header__init(&msg->header)) {
    trans__msg__ActuatorCmds__fini(msg);
    return false;
  }
  // names
  if (!rosidl_runtime_c__String__Sequence__init(&msg->names, 0)) {
    trans__msg__ActuatorCmds__fini(msg);
    return false;
  }
  // gain_p
  if (!rosidl_runtime_c__double__Sequence__init(&msg->gain_p, 0)) {
    trans__msg__ActuatorCmds__fini(msg);
    return false;
  }
  // pos_des
  if (!rosidl_runtime_c__double__Sequence__init(&msg->pos_des, 0)) {
    trans__msg__ActuatorCmds__fini(msg);
    return false;
  }
  // gaid_d
  if (!rosidl_runtime_c__double__Sequence__init(&msg->gaid_d, 0)) {
    trans__msg__ActuatorCmds__fini(msg);
    return false;
  }
  // vel_des
  if (!rosidl_runtime_c__double__Sequence__init(&msg->vel_des, 0)) {
    trans__msg__ActuatorCmds__fini(msg);
    return false;
  }
  // feedforward_torque
  if (!rosidl_runtime_c__double__Sequence__init(&msg->feedforward_torque, 0)) {
    trans__msg__ActuatorCmds__fini(msg);
    return false;
  }
  return true;
}

void
trans__msg__ActuatorCmds__fini(trans__msg__ActuatorCmds * msg)
{
  if (!msg) {
    return;
  }
  // header
  std_msgs__msg__Header__fini(&msg->header);
  // names
  rosidl_runtime_c__String__Sequence__fini(&msg->names);
  // gain_p
  rosidl_runtime_c__double__Sequence__fini(&msg->gain_p);
  // pos_des
  rosidl_runtime_c__double__Sequence__fini(&msg->pos_des);
  // gaid_d
  rosidl_runtime_c__double__Sequence__fini(&msg->gaid_d);
  // vel_des
  rosidl_runtime_c__double__Sequence__fini(&msg->vel_des);
  // feedforward_torque
  rosidl_runtime_c__double__Sequence__fini(&msg->feedforward_torque);
}

bool
trans__msg__ActuatorCmds__are_equal(const trans__msg__ActuatorCmds * lhs, const trans__msg__ActuatorCmds * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // header
  if (!std_msgs__msg__Header__are_equal(
      &(lhs->header), &(rhs->header)))
  {
    return false;
  }
  // names
  if (!rosidl_runtime_c__String__Sequence__are_equal(
      &(lhs->names), &(rhs->names)))
  {
    return false;
  }
  // gain_p
  if (!rosidl_runtime_c__double__Sequence__are_equal(
      &(lhs->gain_p), &(rhs->gain_p)))
  {
    return false;
  }
  // pos_des
  if (!rosidl_runtime_c__double__Sequence__are_equal(
      &(lhs->pos_des), &(rhs->pos_des)))
  {
    return false;
  }
  // gaid_d
  if (!rosidl_runtime_c__double__Sequence__are_equal(
      &(lhs->gaid_d), &(rhs->gaid_d)))
  {
    return false;
  }
  // vel_des
  if (!rosidl_runtime_c__double__Sequence__are_equal(
      &(lhs->vel_des), &(rhs->vel_des)))
  {
    return false;
  }
  // feedforward_torque
  if (!rosidl_runtime_c__double__Sequence__are_equal(
      &(lhs->feedforward_torque), &(rhs->feedforward_torque)))
  {
    return false;
  }
  return true;
}

bool
trans__msg__ActuatorCmds__copy(
  const trans__msg__ActuatorCmds * input,
  trans__msg__ActuatorCmds * output)
{
  if (!input || !output) {
    return false;
  }
  // header
  if (!std_msgs__msg__Header__copy(
      &(input->header), &(output->header)))
  {
    return false;
  }
  // names
  if (!rosidl_runtime_c__String__Sequence__copy(
      &(input->names), &(output->names)))
  {
    return false;
  }
  // gain_p
  if (!rosidl_runtime_c__double__Sequence__copy(
      &(input->gain_p), &(output->gain_p)))
  {
    return false;
  }
  // pos_des
  if (!rosidl_runtime_c__double__Sequence__copy(
      &(input->pos_des), &(output->pos_des)))
  {
    return false;
  }
  // gaid_d
  if (!rosidl_runtime_c__double__Sequence__copy(
      &(input->gaid_d), &(output->gaid_d)))
  {
    return false;
  }
  // vel_des
  if (!rosidl_runtime_c__double__Sequence__copy(
      &(input->vel_des), &(output->vel_des)))
  {
    return false;
  }
  // feedforward_torque
  if (!rosidl_runtime_c__double__Sequence__copy(
      &(input->feedforward_torque), &(output->feedforward_torque)))
  {
    return false;
  }
  return true;
}

trans__msg__ActuatorCmds *
trans__msg__ActuatorCmds__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  trans__msg__ActuatorCmds * msg = (trans__msg__ActuatorCmds *)allocator.allocate(sizeof(trans__msg__ActuatorCmds), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(trans__msg__ActuatorCmds));
  bool success = trans__msg__ActuatorCmds__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
trans__msg__ActuatorCmds__destroy(trans__msg__ActuatorCmds * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    trans__msg__ActuatorCmds__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
trans__msg__ActuatorCmds__Sequence__init(trans__msg__ActuatorCmds__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  trans__msg__ActuatorCmds * data = NULL;

  if (size) {
    data = (trans__msg__ActuatorCmds *)allocator.zero_allocate(size, sizeof(trans__msg__ActuatorCmds), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = trans__msg__ActuatorCmds__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        trans__msg__ActuatorCmds__fini(&data[i - 1]);
      }
      allocator.deallocate(data, allocator.state);
      return false;
    }
  }
  array->data = data;
  array->size = size;
  array->capacity = size;
  return true;
}

void
trans__msg__ActuatorCmds__Sequence__fini(trans__msg__ActuatorCmds__Sequence * array)
{
  if (!array) {
    return;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();

  if (array->data) {
    // ensure that data and capacity values are consistent
    assert(array->capacity > 0);
    // finalize all array elements
    for (size_t i = 0; i < array->capacity; ++i) {
      trans__msg__ActuatorCmds__fini(&array->data[i]);
    }
    allocator.deallocate(array->data, allocator.state);
    array->data = NULL;
    array->size = 0;
    array->capacity = 0;
  } else {
    // ensure that data, size, and capacity values are consistent
    assert(0 == array->size);
    assert(0 == array->capacity);
  }
}

trans__msg__ActuatorCmds__Sequence *
trans__msg__ActuatorCmds__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  trans__msg__ActuatorCmds__Sequence * array = (trans__msg__ActuatorCmds__Sequence *)allocator.allocate(sizeof(trans__msg__ActuatorCmds__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = trans__msg__ActuatorCmds__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
trans__msg__ActuatorCmds__Sequence__destroy(trans__msg__ActuatorCmds__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    trans__msg__ActuatorCmds__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
trans__msg__ActuatorCmds__Sequence__are_equal(const trans__msg__ActuatorCmds__Sequence * lhs, const trans__msg__ActuatorCmds__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!trans__msg__ActuatorCmds__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
trans__msg__ActuatorCmds__Sequence__copy(
  const trans__msg__ActuatorCmds__Sequence * input,
  trans__msg__ActuatorCmds__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(trans__msg__ActuatorCmds);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    trans__msg__ActuatorCmds * data =
      (trans__msg__ActuatorCmds *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!trans__msg__ActuatorCmds__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          trans__msg__ActuatorCmds__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!trans__msg__ActuatorCmds__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}
