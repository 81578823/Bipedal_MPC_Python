// generated from rosidl_generator_c/resource/idl__functions.h.em
// with input from trans:msg/ActuatorCmds.idl
// generated code does not contain a copyright notice

#ifndef TRANS__MSG__DETAIL__ACTUATOR_CMDS__FUNCTIONS_H_
#define TRANS__MSG__DETAIL__ACTUATOR_CMDS__FUNCTIONS_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stdlib.h>

#include "rosidl_runtime_c/visibility_control.h"
#include "trans/msg/rosidl_generator_c__visibility_control.h"

#include "trans/msg/detail/actuator_cmds__struct.h"

/// Initialize msg/ActuatorCmds message.
/**
 * If the init function is called twice for the same message without
 * calling fini inbetween previously allocated memory will be leaked.
 * \param[in,out] msg The previously allocated message pointer.
 * Fields without a default value will not be initialized by this function.
 * You might want to call memset(msg, 0, sizeof(
 * trans__msg__ActuatorCmds
 * )) before or use
 * trans__msg__ActuatorCmds__create()
 * to allocate and initialize the message.
 * \return true if initialization was successful, otherwise false
 */
ROSIDL_GENERATOR_C_PUBLIC_trans
bool
trans__msg__ActuatorCmds__init(trans__msg__ActuatorCmds * msg);

/// Finalize msg/ActuatorCmds message.
/**
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_trans
void
trans__msg__ActuatorCmds__fini(trans__msg__ActuatorCmds * msg);

/// Create msg/ActuatorCmds message.
/**
 * It allocates the memory for the message, sets the memory to zero, and
 * calls
 * trans__msg__ActuatorCmds__init().
 * \return The pointer to the initialized message if successful,
 * otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_trans
trans__msg__ActuatorCmds *
trans__msg__ActuatorCmds__create();

/// Destroy msg/ActuatorCmds message.
/**
 * It calls
 * trans__msg__ActuatorCmds__fini()
 * and frees the memory of the message.
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_trans
void
trans__msg__ActuatorCmds__destroy(trans__msg__ActuatorCmds * msg);

/// Check for msg/ActuatorCmds message equality.
/**
 * \param[in] lhs The message on the left hand size of the equality operator.
 * \param[in] rhs The message on the right hand size of the equality operator.
 * \return true if messages are equal, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_trans
bool
trans__msg__ActuatorCmds__are_equal(const trans__msg__ActuatorCmds * lhs, const trans__msg__ActuatorCmds * rhs);

/// Copy a msg/ActuatorCmds message.
/**
 * This functions performs a deep copy, as opposed to the shallow copy that
 * plain assignment yields.
 *
 * \param[in] input The source message pointer.
 * \param[out] output The target message pointer, which must
 *   have been initialized before calling this function.
 * \return true if successful, or false if either pointer is null
 *   or memory allocation fails.
 */
ROSIDL_GENERATOR_C_PUBLIC_trans
bool
trans__msg__ActuatorCmds__copy(
  const trans__msg__ActuatorCmds * input,
  trans__msg__ActuatorCmds * output);

/// Initialize array of msg/ActuatorCmds messages.
/**
 * It allocates the memory for the number of elements and calls
 * trans__msg__ActuatorCmds__init()
 * for each element of the array.
 * \param[in,out] array The allocated array pointer.
 * \param[in] size The size / capacity of the array.
 * \return true if initialization was successful, otherwise false
 * If the array pointer is valid and the size is zero it is guaranteed
 # to return true.
 */
ROSIDL_GENERATOR_C_PUBLIC_trans
bool
trans__msg__ActuatorCmds__Sequence__init(trans__msg__ActuatorCmds__Sequence * array, size_t size);

/// Finalize array of msg/ActuatorCmds messages.
/**
 * It calls
 * trans__msg__ActuatorCmds__fini()
 * for each element of the array and frees the memory for the number of
 * elements.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_trans
void
trans__msg__ActuatorCmds__Sequence__fini(trans__msg__ActuatorCmds__Sequence * array);

/// Create array of msg/ActuatorCmds messages.
/**
 * It allocates the memory for the array and calls
 * trans__msg__ActuatorCmds__Sequence__init().
 * \param[in] size The size / capacity of the array.
 * \return The pointer to the initialized array if successful, otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_trans
trans__msg__ActuatorCmds__Sequence *
trans__msg__ActuatorCmds__Sequence__create(size_t size);

/// Destroy array of msg/ActuatorCmds messages.
/**
 * It calls
 * trans__msg__ActuatorCmds__Sequence__fini()
 * on the array,
 * and frees the memory of the array.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_trans
void
trans__msg__ActuatorCmds__Sequence__destroy(trans__msg__ActuatorCmds__Sequence * array);

/// Check for msg/ActuatorCmds message array equality.
/**
 * \param[in] lhs The message array on the left hand size of the equality operator.
 * \param[in] rhs The message array on the right hand size of the equality operator.
 * \return true if message arrays are equal in size and content, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_trans
bool
trans__msg__ActuatorCmds__Sequence__are_equal(const trans__msg__ActuatorCmds__Sequence * lhs, const trans__msg__ActuatorCmds__Sequence * rhs);

/// Copy an array of msg/ActuatorCmds messages.
/**
 * This functions performs a deep copy, as opposed to the shallow copy that
 * plain assignment yields.
 *
 * \param[in] input The source array pointer.
 * \param[out] output The target array pointer, which must
 *   have been initialized before calling this function.
 * \return true if successful, or false if either pointer
 *   is null or memory allocation fails.
 */
ROSIDL_GENERATOR_C_PUBLIC_trans
bool
trans__msg__ActuatorCmds__Sequence__copy(
  const trans__msg__ActuatorCmds__Sequence * input,
  trans__msg__ActuatorCmds__Sequence * output);

#ifdef __cplusplus
}
#endif

#endif  // TRANS__MSG__DETAIL__ACTUATOR_CMDS__FUNCTIONS_H_
