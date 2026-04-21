// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from gp7_task_executor_msgs:srv/MoveSequence.idl
// generated code does not contain a copyright notice

#ifndef GP7_TASK_EXECUTOR_MSGS__SRV__DETAIL__MOVE_SEQUENCE__STRUCT_H_
#define GP7_TASK_EXECUTOR_MSGS__SRV__DETAIL__MOVE_SEQUENCE__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

/// Struct defined in srv/MoveSequence in the package gp7_task_executor_msgs.
typedef struct gp7_task_executor_msgs__srv__MoveSequence_Request
{
  bool execute;
} gp7_task_executor_msgs__srv__MoveSequence_Request;

// Struct for a sequence of gp7_task_executor_msgs__srv__MoveSequence_Request.
typedef struct gp7_task_executor_msgs__srv__MoveSequence_Request__Sequence
{
  gp7_task_executor_msgs__srv__MoveSequence_Request * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} gp7_task_executor_msgs__srv__MoveSequence_Request__Sequence;


// Constants defined in the message

// Include directives for member types
// Member 'message'
#include "rosidl_runtime_c/string.h"

/// Struct defined in srv/MoveSequence in the package gp7_task_executor_msgs.
typedef struct gp7_task_executor_msgs__srv__MoveSequence_Response
{
  bool success;
  rosidl_runtime_c__String message;
} gp7_task_executor_msgs__srv__MoveSequence_Response;

// Struct for a sequence of gp7_task_executor_msgs__srv__MoveSequence_Response.
typedef struct gp7_task_executor_msgs__srv__MoveSequence_Response__Sequence
{
  gp7_task_executor_msgs__srv__MoveSequence_Response * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} gp7_task_executor_msgs__srv__MoveSequence_Response__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // GP7_TASK_EXECUTOR_MSGS__SRV__DETAIL__MOVE_SEQUENCE__STRUCT_H_
