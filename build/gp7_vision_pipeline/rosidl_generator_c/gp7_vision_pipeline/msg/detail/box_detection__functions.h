// generated from rosidl_generator_c/resource/idl__functions.h.em
// with input from gp7_vision_pipeline:msg/BoxDetection.idl
// generated code does not contain a copyright notice

#ifndef GP7_VISION_PIPELINE__MSG__DETAIL__BOX_DETECTION__FUNCTIONS_H_
#define GP7_VISION_PIPELINE__MSG__DETAIL__BOX_DETECTION__FUNCTIONS_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stdlib.h>

#include "rosidl_runtime_c/visibility_control.h"
#include "gp7_vision_pipeline/msg/rosidl_generator_c__visibility_control.h"

#include "gp7_vision_pipeline/msg/detail/box_detection__struct.h"

/// Initialize msg/BoxDetection message.
/**
 * If the init function is called twice for the same message without
 * calling fini inbetween previously allocated memory will be leaked.
 * \param[in,out] msg The previously allocated message pointer.
 * Fields without a default value will not be initialized by this function.
 * You might want to call memset(msg, 0, sizeof(
 * gp7_vision_pipeline__msg__BoxDetection
 * )) before or use
 * gp7_vision_pipeline__msg__BoxDetection__create()
 * to allocate and initialize the message.
 * \return true if initialization was successful, otherwise false
 */
ROSIDL_GENERATOR_C_PUBLIC_gp7_vision_pipeline
bool
gp7_vision_pipeline__msg__BoxDetection__init(gp7_vision_pipeline__msg__BoxDetection * msg);

/// Finalize msg/BoxDetection message.
/**
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_gp7_vision_pipeline
void
gp7_vision_pipeline__msg__BoxDetection__fini(gp7_vision_pipeline__msg__BoxDetection * msg);

/// Create msg/BoxDetection message.
/**
 * It allocates the memory for the message, sets the memory to zero, and
 * calls
 * gp7_vision_pipeline__msg__BoxDetection__init().
 * \return The pointer to the initialized message if successful,
 * otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_gp7_vision_pipeline
gp7_vision_pipeline__msg__BoxDetection *
gp7_vision_pipeline__msg__BoxDetection__create();

/// Destroy msg/BoxDetection message.
/**
 * It calls
 * gp7_vision_pipeline__msg__BoxDetection__fini()
 * and frees the memory of the message.
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_gp7_vision_pipeline
void
gp7_vision_pipeline__msg__BoxDetection__destroy(gp7_vision_pipeline__msg__BoxDetection * msg);

/// Check for msg/BoxDetection message equality.
/**
 * \param[in] lhs The message on the left hand size of the equality operator.
 * \param[in] rhs The message on the right hand size of the equality operator.
 * \return true if messages are equal, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_gp7_vision_pipeline
bool
gp7_vision_pipeline__msg__BoxDetection__are_equal(const gp7_vision_pipeline__msg__BoxDetection * lhs, const gp7_vision_pipeline__msg__BoxDetection * rhs);

/// Copy a msg/BoxDetection message.
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
ROSIDL_GENERATOR_C_PUBLIC_gp7_vision_pipeline
bool
gp7_vision_pipeline__msg__BoxDetection__copy(
  const gp7_vision_pipeline__msg__BoxDetection * input,
  gp7_vision_pipeline__msg__BoxDetection * output);

/// Initialize array of msg/BoxDetection messages.
/**
 * It allocates the memory for the number of elements and calls
 * gp7_vision_pipeline__msg__BoxDetection__init()
 * for each element of the array.
 * \param[in,out] array The allocated array pointer.
 * \param[in] size The size / capacity of the array.
 * \return true if initialization was successful, otherwise false
 * If the array pointer is valid and the size is zero it is guaranteed
 # to return true.
 */
ROSIDL_GENERATOR_C_PUBLIC_gp7_vision_pipeline
bool
gp7_vision_pipeline__msg__BoxDetection__Sequence__init(gp7_vision_pipeline__msg__BoxDetection__Sequence * array, size_t size);

/// Finalize array of msg/BoxDetection messages.
/**
 * It calls
 * gp7_vision_pipeline__msg__BoxDetection__fini()
 * for each element of the array and frees the memory for the number of
 * elements.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_gp7_vision_pipeline
void
gp7_vision_pipeline__msg__BoxDetection__Sequence__fini(gp7_vision_pipeline__msg__BoxDetection__Sequence * array);

/// Create array of msg/BoxDetection messages.
/**
 * It allocates the memory for the array and calls
 * gp7_vision_pipeline__msg__BoxDetection__Sequence__init().
 * \param[in] size The size / capacity of the array.
 * \return The pointer to the initialized array if successful, otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_gp7_vision_pipeline
gp7_vision_pipeline__msg__BoxDetection__Sequence *
gp7_vision_pipeline__msg__BoxDetection__Sequence__create(size_t size);

/// Destroy array of msg/BoxDetection messages.
/**
 * It calls
 * gp7_vision_pipeline__msg__BoxDetection__Sequence__fini()
 * on the array,
 * and frees the memory of the array.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_gp7_vision_pipeline
void
gp7_vision_pipeline__msg__BoxDetection__Sequence__destroy(gp7_vision_pipeline__msg__BoxDetection__Sequence * array);

/// Check for msg/BoxDetection message array equality.
/**
 * \param[in] lhs The message array on the left hand size of the equality operator.
 * \param[in] rhs The message array on the right hand size of the equality operator.
 * \return true if message arrays are equal in size and content, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_gp7_vision_pipeline
bool
gp7_vision_pipeline__msg__BoxDetection__Sequence__are_equal(const gp7_vision_pipeline__msg__BoxDetection__Sequence * lhs, const gp7_vision_pipeline__msg__BoxDetection__Sequence * rhs);

/// Copy an array of msg/BoxDetection messages.
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
ROSIDL_GENERATOR_C_PUBLIC_gp7_vision_pipeline
bool
gp7_vision_pipeline__msg__BoxDetection__Sequence__copy(
  const gp7_vision_pipeline__msg__BoxDetection__Sequence * input,
  gp7_vision_pipeline__msg__BoxDetection__Sequence * output);

#ifdef __cplusplus
}
#endif

#endif  // GP7_VISION_PIPELINE__MSG__DETAIL__BOX_DETECTION__FUNCTIONS_H_
