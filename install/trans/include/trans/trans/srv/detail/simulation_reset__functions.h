// generated from rosidl_generator_c/resource/idl__functions.h.em
// with input from trans:srv/SimulationReset.idl
// generated code does not contain a copyright notice

#ifndef TRANS__SRV__DETAIL__SIMULATION_RESET__FUNCTIONS_H_
#define TRANS__SRV__DETAIL__SIMULATION_RESET__FUNCTIONS_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stdlib.h>

#include "rosidl_runtime_c/visibility_control.h"
#include "trans/msg/rosidl_generator_c__visibility_control.h"

#include "trans/srv/detail/simulation_reset__struct.h"

/// Initialize srv/SimulationReset message.
/**
 * If the init function is called twice for the same message without
 * calling fini inbetween previously allocated memory will be leaked.
 * \param[in,out] msg The previously allocated message pointer.
 * Fields without a default value will not be initialized by this function.
 * You might want to call memset(msg, 0, sizeof(
 * trans__srv__SimulationReset_Request
 * )) before or use
 * trans__srv__SimulationReset_Request__create()
 * to allocate and initialize the message.
 * \return true if initialization was successful, otherwise false
 */
ROSIDL_GENERATOR_C_PUBLIC_trans
bool
trans__srv__SimulationReset_Request__init(trans__srv__SimulationReset_Request * msg);

/// Finalize srv/SimulationReset message.
/**
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_trans
void
trans__srv__SimulationReset_Request__fini(trans__srv__SimulationReset_Request * msg);

/// Create srv/SimulationReset message.
/**
 * It allocates the memory for the message, sets the memory to zero, and
 * calls
 * trans__srv__SimulationReset_Request__init().
 * \return The pointer to the initialized message if successful,
 * otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_trans
trans__srv__SimulationReset_Request *
trans__srv__SimulationReset_Request__create();

/// Destroy srv/SimulationReset message.
/**
 * It calls
 * trans__srv__SimulationReset_Request__fini()
 * and frees the memory of the message.
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_trans
void
trans__srv__SimulationReset_Request__destroy(trans__srv__SimulationReset_Request * msg);

/// Check for srv/SimulationReset message equality.
/**
 * \param[in] lhs The message on the left hand size of the equality operator.
 * \param[in] rhs The message on the right hand size of the equality operator.
 * \return true if messages are equal, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_trans
bool
trans__srv__SimulationReset_Request__are_equal(const trans__srv__SimulationReset_Request * lhs, const trans__srv__SimulationReset_Request * rhs);

/// Copy a srv/SimulationReset message.
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
trans__srv__SimulationReset_Request__copy(
  const trans__srv__SimulationReset_Request * input,
  trans__srv__SimulationReset_Request * output);

/// Initialize array of srv/SimulationReset messages.
/**
 * It allocates the memory for the number of elements and calls
 * trans__srv__SimulationReset_Request__init()
 * for each element of the array.
 * \param[in,out] array The allocated array pointer.
 * \param[in] size The size / capacity of the array.
 * \return true if initialization was successful, otherwise false
 * If the array pointer is valid and the size is zero it is guaranteed
 # to return true.
 */
ROSIDL_GENERATOR_C_PUBLIC_trans
bool
trans__srv__SimulationReset_Request__Sequence__init(trans__srv__SimulationReset_Request__Sequence * array, size_t size);

/// Finalize array of srv/SimulationReset messages.
/**
 * It calls
 * trans__srv__SimulationReset_Request__fini()
 * for each element of the array and frees the memory for the number of
 * elements.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_trans
void
trans__srv__SimulationReset_Request__Sequence__fini(trans__srv__SimulationReset_Request__Sequence * array);

/// Create array of srv/SimulationReset messages.
/**
 * It allocates the memory for the array and calls
 * trans__srv__SimulationReset_Request__Sequence__init().
 * \param[in] size The size / capacity of the array.
 * \return The pointer to the initialized array if successful, otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_trans
trans__srv__SimulationReset_Request__Sequence *
trans__srv__SimulationReset_Request__Sequence__create(size_t size);

/// Destroy array of srv/SimulationReset messages.
/**
 * It calls
 * trans__srv__SimulationReset_Request__Sequence__fini()
 * on the array,
 * and frees the memory of the array.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_trans
void
trans__srv__SimulationReset_Request__Sequence__destroy(trans__srv__SimulationReset_Request__Sequence * array);

/// Check for srv/SimulationReset message array equality.
/**
 * \param[in] lhs The message array on the left hand size of the equality operator.
 * \param[in] rhs The message array on the right hand size of the equality operator.
 * \return true if message arrays are equal in size and content, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_trans
bool
trans__srv__SimulationReset_Request__Sequence__are_equal(const trans__srv__SimulationReset_Request__Sequence * lhs, const trans__srv__SimulationReset_Request__Sequence * rhs);

/// Copy an array of srv/SimulationReset messages.
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
trans__srv__SimulationReset_Request__Sequence__copy(
  const trans__srv__SimulationReset_Request__Sequence * input,
  trans__srv__SimulationReset_Request__Sequence * output);

/// Initialize srv/SimulationReset message.
/**
 * If the init function is called twice for the same message without
 * calling fini inbetween previously allocated memory will be leaked.
 * \param[in,out] msg The previously allocated message pointer.
 * Fields without a default value will not be initialized by this function.
 * You might want to call memset(msg, 0, sizeof(
 * trans__srv__SimulationReset_Response
 * )) before or use
 * trans__srv__SimulationReset_Response__create()
 * to allocate and initialize the message.
 * \return true if initialization was successful, otherwise false
 */
ROSIDL_GENERATOR_C_PUBLIC_trans
bool
trans__srv__SimulationReset_Response__init(trans__srv__SimulationReset_Response * msg);

/// Finalize srv/SimulationReset message.
/**
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_trans
void
trans__srv__SimulationReset_Response__fini(trans__srv__SimulationReset_Response * msg);

/// Create srv/SimulationReset message.
/**
 * It allocates the memory for the message, sets the memory to zero, and
 * calls
 * trans__srv__SimulationReset_Response__init().
 * \return The pointer to the initialized message if successful,
 * otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_trans
trans__srv__SimulationReset_Response *
trans__srv__SimulationReset_Response__create();

/// Destroy srv/SimulationReset message.
/**
 * It calls
 * trans__srv__SimulationReset_Response__fini()
 * and frees the memory of the message.
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_trans
void
trans__srv__SimulationReset_Response__destroy(trans__srv__SimulationReset_Response * msg);

/// Check for srv/SimulationReset message equality.
/**
 * \param[in] lhs The message on the left hand size of the equality operator.
 * \param[in] rhs The message on the right hand size of the equality operator.
 * \return true if messages are equal, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_trans
bool
trans__srv__SimulationReset_Response__are_equal(const trans__srv__SimulationReset_Response * lhs, const trans__srv__SimulationReset_Response * rhs);

/// Copy a srv/SimulationReset message.
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
trans__srv__SimulationReset_Response__copy(
  const trans__srv__SimulationReset_Response * input,
  trans__srv__SimulationReset_Response * output);

/// Initialize array of srv/SimulationReset messages.
/**
 * It allocates the memory for the number of elements and calls
 * trans__srv__SimulationReset_Response__init()
 * for each element of the array.
 * \param[in,out] array The allocated array pointer.
 * \param[in] size The size / capacity of the array.
 * \return true if initialization was successful, otherwise false
 * If the array pointer is valid and the size is zero it is guaranteed
 # to return true.
 */
ROSIDL_GENERATOR_C_PUBLIC_trans
bool
trans__srv__SimulationReset_Response__Sequence__init(trans__srv__SimulationReset_Response__Sequence * array, size_t size);

/// Finalize array of srv/SimulationReset messages.
/**
 * It calls
 * trans__srv__SimulationReset_Response__fini()
 * for each element of the array and frees the memory for the number of
 * elements.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_trans
void
trans__srv__SimulationReset_Response__Sequence__fini(trans__srv__SimulationReset_Response__Sequence * array);

/// Create array of srv/SimulationReset messages.
/**
 * It allocates the memory for the array and calls
 * trans__srv__SimulationReset_Response__Sequence__init().
 * \param[in] size The size / capacity of the array.
 * \return The pointer to the initialized array if successful, otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_trans
trans__srv__SimulationReset_Response__Sequence *
trans__srv__SimulationReset_Response__Sequence__create(size_t size);

/// Destroy array of srv/SimulationReset messages.
/**
 * It calls
 * trans__srv__SimulationReset_Response__Sequence__fini()
 * on the array,
 * and frees the memory of the array.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_trans
void
trans__srv__SimulationReset_Response__Sequence__destroy(trans__srv__SimulationReset_Response__Sequence * array);

/// Check for srv/SimulationReset message array equality.
/**
 * \param[in] lhs The message array on the left hand size of the equality operator.
 * \param[in] rhs The message array on the right hand size of the equality operator.
 * \return true if message arrays are equal in size and content, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_trans
bool
trans__srv__SimulationReset_Response__Sequence__are_equal(const trans__srv__SimulationReset_Response__Sequence * lhs, const trans__srv__SimulationReset_Response__Sequence * rhs);

/// Copy an array of srv/SimulationReset messages.
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
trans__srv__SimulationReset_Response__Sequence__copy(
  const trans__srv__SimulationReset_Response__Sequence * input,
  trans__srv__SimulationReset_Response__Sequence * output);

#ifdef __cplusplus
}
#endif

#endif  // TRANS__SRV__DETAIL__SIMULATION_RESET__FUNCTIONS_H_
