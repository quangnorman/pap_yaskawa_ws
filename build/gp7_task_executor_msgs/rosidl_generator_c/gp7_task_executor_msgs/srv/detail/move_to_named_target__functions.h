// generated from rosidl_generator_c/resource/idl__functions.h.em
// with input from gp7_task_executor_msgs:srv/MoveToNamedTarget.idl
// generated code does not contain a copyright notice

#ifndef GP7_TASK_EXECUTOR_MSGS__SRV__DETAIL__MOVE_TO_NAMED_TARGET__FUNCTIONS_H_
#define GP7_TASK_EXECUTOR_MSGS__SRV__DETAIL__MOVE_TO_NAMED_TARGET__FUNCTIONS_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stdlib.h>

#include "rosidl_runtime_c/visibility_control.h"
#include "gp7_task_executor_msgs/msg/rosidl_generator_c__visibility_control.h"

#include "gp7_task_executor_msgs/srv/detail/move_to_named_target__struct.h"

/// Initialize srv/MoveToNamedTarget message.
/**
 * If the init function is called twice for the same message without
 * calling fini inbetween previously allocated memory will be leaked.
 * \param[in,out] msg The previously allocated message pointer.
 * Fields without a default value will not be initialized by this function.
 * You might want to call memset(msg, 0, sizeof(
 * gp7_task_executor_msgs__srv__MoveToNamedTarget_Request
 * )) before or use
 * gp7_task_executor_msgs__srv__MoveToNamedTarget_Request__create()
 * to allocate and initialize the message.
 * \return true if initialization was successful, otherwise false
 */
ROSIDL_GENERATOR_C_PUBLIC_gp7_task_executor_msgs
bool
gp7_task_executor_msgs__srv__MoveToNamedTarget_Request__init(gp7_task_executor_msgs__srv__MoveToNamedTarget_Request * msg);

/// Finalize srv/MoveToNamedTarget message.
/**
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_gp7_task_executor_msgs
void
gp7_task_executor_msgs__srv__MoveToNamedTarget_Request__fini(gp7_task_executor_msgs__srv__MoveToNamedTarget_Request * msg);

/// Create srv/MoveToNamedTarget message.
/**
 * It allocates the memory for the message, sets the memory to zero, and
 * calls
 * gp7_task_executor_msgs__srv__MoveToNamedTarget_Request__init().
 * \return The pointer to the initialized message if successful,
 * otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_gp7_task_executor_msgs
gp7_task_executor_msgs__srv__MoveToNamedTarget_Request *
gp7_task_executor_msgs__srv__MoveToNamedTarget_Request__create();

/// Destroy srv/MoveToNamedTarget message.
/**
 * It calls
 * gp7_task_executor_msgs__srv__MoveToNamedTarget_Request__fini()
 * and frees the memory of the message.
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_gp7_task_executor_msgs
void
gp7_task_executor_msgs__srv__MoveToNamedTarget_Request__destroy(gp7_task_executor_msgs__srv__MoveToNamedTarget_Request * msg);

/// Check for srv/MoveToNamedTarget message equality.
/**
 * \param[in] lhs The message on the left hand size of the equality operator.
 * \param[in] rhs The message on the right hand size of the equality operator.
 * \return true if messages are equal, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_gp7_task_executor_msgs
bool
gp7_task_executor_msgs__srv__MoveToNamedTarget_Request__are_equal(const gp7_task_executor_msgs__srv__MoveToNamedTarget_Request * lhs, const gp7_task_executor_msgs__srv__MoveToNamedTarget_Request * rhs);

/// Copy a srv/MoveToNamedTarget message.
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
ROSIDL_GENERATOR_C_PUBLIC_gp7_task_executor_msgs
bool
gp7_task_executor_msgs__srv__MoveToNamedTarget_Request__copy(
  const gp7_task_executor_msgs__srv__MoveToNamedTarget_Request * input,
  gp7_task_executor_msgs__srv__MoveToNamedTarget_Request * output);

/// Initialize array of srv/MoveToNamedTarget messages.
/**
 * It allocates the memory for the number of elements and calls
 * gp7_task_executor_msgs__srv__MoveToNamedTarget_Request__init()
 * for each element of the array.
 * \param[in,out] array The allocated array pointer.
 * \param[in] size The size / capacity of the array.
 * \return true if initialization was successful, otherwise false
 * If the array pointer is valid and the size is zero it is guaranteed
 # to return true.
 */
ROSIDL_GENERATOR_C_PUBLIC_gp7_task_executor_msgs
bool
gp7_task_executor_msgs__srv__MoveToNamedTarget_Request__Sequence__init(gp7_task_executor_msgs__srv__MoveToNamedTarget_Request__Sequence * array, size_t size);

/// Finalize array of srv/MoveToNamedTarget messages.
/**
 * It calls
 * gp7_task_executor_msgs__srv__MoveToNamedTarget_Request__fini()
 * for each element of the array and frees the memory for the number of
 * elements.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_gp7_task_executor_msgs
void
gp7_task_executor_msgs__srv__MoveToNamedTarget_Request__Sequence__fini(gp7_task_executor_msgs__srv__MoveToNamedTarget_Request__Sequence * array);

/// Create array of srv/MoveToNamedTarget messages.
/**
 * It allocates the memory for the array and calls
 * gp7_task_executor_msgs__srv__MoveToNamedTarget_Request__Sequence__init().
 * \param[in] size The size / capacity of the array.
 * \return The pointer to the initialized array if successful, otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_gp7_task_executor_msgs
gp7_task_executor_msgs__srv__MoveToNamedTarget_Request__Sequence *
gp7_task_executor_msgs__srv__MoveToNamedTarget_Request__Sequence__create(size_t size);

/// Destroy array of srv/MoveToNamedTarget messages.
/**
 * It calls
 * gp7_task_executor_msgs__srv__MoveToNamedTarget_Request__Sequence__fini()
 * on the array,
 * and frees the memory of the array.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_gp7_task_executor_msgs
void
gp7_task_executor_msgs__srv__MoveToNamedTarget_Request__Sequence__destroy(gp7_task_executor_msgs__srv__MoveToNamedTarget_Request__Sequence * array);

/// Check for srv/MoveToNamedTarget message array equality.
/**
 * \param[in] lhs The message array on the left hand size of the equality operator.
 * \param[in] rhs The message array on the right hand size of the equality operator.
 * \return true if message arrays are equal in size and content, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_gp7_task_executor_msgs
bool
gp7_task_executor_msgs__srv__MoveToNamedTarget_Request__Sequence__are_equal(const gp7_task_executor_msgs__srv__MoveToNamedTarget_Request__Sequence * lhs, const gp7_task_executor_msgs__srv__MoveToNamedTarget_Request__Sequence * rhs);

/// Copy an array of srv/MoveToNamedTarget messages.
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
ROSIDL_GENERATOR_C_PUBLIC_gp7_task_executor_msgs
bool
gp7_task_executor_msgs__srv__MoveToNamedTarget_Request__Sequence__copy(
  const gp7_task_executor_msgs__srv__MoveToNamedTarget_Request__Sequence * input,
  gp7_task_executor_msgs__srv__MoveToNamedTarget_Request__Sequence * output);

/// Initialize srv/MoveToNamedTarget message.
/**
 * If the init function is called twice for the same message without
 * calling fini inbetween previously allocated memory will be leaked.
 * \param[in,out] msg The previously allocated message pointer.
 * Fields without a default value will not be initialized by this function.
 * You might want to call memset(msg, 0, sizeof(
 * gp7_task_executor_msgs__srv__MoveToNamedTarget_Response
 * )) before or use
 * gp7_task_executor_msgs__srv__MoveToNamedTarget_Response__create()
 * to allocate and initialize the message.
 * \return true if initialization was successful, otherwise false
 */
ROSIDL_GENERATOR_C_PUBLIC_gp7_task_executor_msgs
bool
gp7_task_executor_msgs__srv__MoveToNamedTarget_Response__init(gp7_task_executor_msgs__srv__MoveToNamedTarget_Response * msg);

/// Finalize srv/MoveToNamedTarget message.
/**
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_gp7_task_executor_msgs
void
gp7_task_executor_msgs__srv__MoveToNamedTarget_Response__fini(gp7_task_executor_msgs__srv__MoveToNamedTarget_Response * msg);

/// Create srv/MoveToNamedTarget message.
/**
 * It allocates the memory for the message, sets the memory to zero, and
 * calls
 * gp7_task_executor_msgs__srv__MoveToNamedTarget_Response__init().
 * \return The pointer to the initialized message if successful,
 * otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_gp7_task_executor_msgs
gp7_task_executor_msgs__srv__MoveToNamedTarget_Response *
gp7_task_executor_msgs__srv__MoveToNamedTarget_Response__create();

/// Destroy srv/MoveToNamedTarget message.
/**
 * It calls
 * gp7_task_executor_msgs__srv__MoveToNamedTarget_Response__fini()
 * and frees the memory of the message.
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_gp7_task_executor_msgs
void
gp7_task_executor_msgs__srv__MoveToNamedTarget_Response__destroy(gp7_task_executor_msgs__srv__MoveToNamedTarget_Response * msg);

/// Check for srv/MoveToNamedTarget message equality.
/**
 * \param[in] lhs The message on the left hand size of the equality operator.
 * \param[in] rhs The message on the right hand size of the equality operator.
 * \return true if messages are equal, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_gp7_task_executor_msgs
bool
gp7_task_executor_msgs__srv__MoveToNamedTarget_Response__are_equal(const gp7_task_executor_msgs__srv__MoveToNamedTarget_Response * lhs, const gp7_task_executor_msgs__srv__MoveToNamedTarget_Response * rhs);

/// Copy a srv/MoveToNamedTarget message.
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
ROSIDL_GENERATOR_C_PUBLIC_gp7_task_executor_msgs
bool
gp7_task_executor_msgs__srv__MoveToNamedTarget_Response__copy(
  const gp7_task_executor_msgs__srv__MoveToNamedTarget_Response * input,
  gp7_task_executor_msgs__srv__MoveToNamedTarget_Response * output);

/// Initialize array of srv/MoveToNamedTarget messages.
/**
 * It allocates the memory for the number of elements and calls
 * gp7_task_executor_msgs__srv__MoveToNamedTarget_Response__init()
 * for each element of the array.
 * \param[in,out] array The allocated array pointer.
 * \param[in] size The size / capacity of the array.
 * \return true if initialization was successful, otherwise false
 * If the array pointer is valid and the size is zero it is guaranteed
 # to return true.
 */
ROSIDL_GENERATOR_C_PUBLIC_gp7_task_executor_msgs
bool
gp7_task_executor_msgs__srv__MoveToNamedTarget_Response__Sequence__init(gp7_task_executor_msgs__srv__MoveToNamedTarget_Response__Sequence * array, size_t size);

/// Finalize array of srv/MoveToNamedTarget messages.
/**
 * It calls
 * gp7_task_executor_msgs__srv__MoveToNamedTarget_Response__fini()
 * for each element of the array and frees the memory for the number of
 * elements.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_gp7_task_executor_msgs
void
gp7_task_executor_msgs__srv__MoveToNamedTarget_Response__Sequence__fini(gp7_task_executor_msgs__srv__MoveToNamedTarget_Response__Sequence * array);

/// Create array of srv/MoveToNamedTarget messages.
/**
 * It allocates the memory for the array and calls
 * gp7_task_executor_msgs__srv__MoveToNamedTarget_Response__Sequence__init().
 * \param[in] size The size / capacity of the array.
 * \return The pointer to the initialized array if successful, otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_gp7_task_executor_msgs
gp7_task_executor_msgs__srv__MoveToNamedTarget_Response__Sequence *
gp7_task_executor_msgs__srv__MoveToNamedTarget_Response__Sequence__create(size_t size);

/// Destroy array of srv/MoveToNamedTarget messages.
/**
 * It calls
 * gp7_task_executor_msgs__srv__MoveToNamedTarget_Response__Sequence__fini()
 * on the array,
 * and frees the memory of the array.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_gp7_task_executor_msgs
void
gp7_task_executor_msgs__srv__MoveToNamedTarget_Response__Sequence__destroy(gp7_task_executor_msgs__srv__MoveToNamedTarget_Response__Sequence * array);

/// Check for srv/MoveToNamedTarget message array equality.
/**
 * \param[in] lhs The message array on the left hand size of the equality operator.
 * \param[in] rhs The message array on the right hand size of the equality operator.
 * \return true if message arrays are equal in size and content, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_gp7_task_executor_msgs
bool
gp7_task_executor_msgs__srv__MoveToNamedTarget_Response__Sequence__are_equal(const gp7_task_executor_msgs__srv__MoveToNamedTarget_Response__Sequence * lhs, const gp7_task_executor_msgs__srv__MoveToNamedTarget_Response__Sequence * rhs);

/// Copy an array of srv/MoveToNamedTarget messages.
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
ROSIDL_GENERATOR_C_PUBLIC_gp7_task_executor_msgs
bool
gp7_task_executor_msgs__srv__MoveToNamedTarget_Response__Sequence__copy(
  const gp7_task_executor_msgs__srv__MoveToNamedTarget_Response__Sequence * input,
  gp7_task_executor_msgs__srv__MoveToNamedTarget_Response__Sequence * output);

#ifdef __cplusplus
}
#endif

#endif  // GP7_TASK_EXECUTOR_MSGS__SRV__DETAIL__MOVE_TO_NAMED_TARGET__FUNCTIONS_H_
