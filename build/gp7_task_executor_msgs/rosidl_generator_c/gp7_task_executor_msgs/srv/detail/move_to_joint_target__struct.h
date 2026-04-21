// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from gp7_task_executor_msgs:srv/MoveToJointTarget.idl
// generated code does not contain a copyright notice

#ifndef GP7_TASK_EXECUTOR_MSGS__SRV__DETAIL__MOVE_TO_JOINT_TARGET__STRUCT_H_
#define GP7_TASK_EXECUTOR_MSGS__SRV__DETAIL__MOVE_TO_JOINT_TARGET__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

// Include directives for member types
// Member 'joint_names'
#include "rosidl_runtime_c/string.h"
// Member 'positions'
#include "rosidl_runtime_c/primitives_sequence.h"

/// Struct defined in srv/MoveToJointTarget in the package gp7_task_executor_msgs.
typedef struct gp7_task_executor_msgs__srv__MoveToJointTarget_Request
{
  rosidl_runtime_c__String__Sequence joint_names;
  rosidl_runtime_c__double__Sequence positions;
  bool execute;
} gp7_task_executor_msgs__srv__MoveToJointTarget_Request;

// Struct for a sequence of gp7_task_executor_msgs__srv__MoveToJointTarget_Request.
typedef struct gp7_task_executor_msgs__srv__MoveToJointTarget_Request__Sequence
{
  gp7_task_executor_msgs__srv__MoveToJointTarget_Request * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} gp7_task_executor_msgs__srv__MoveToJointTarget_Request__Sequence;


// Constants defined in the message

// Include directives for member types
// Member 'message'
// already included above
// #include "rosidl_runtime_c/string.h"

/// Struct defined in srv/MoveToJointTarget in the package gp7_task_executor_msgs.
typedef struct gp7_task_executor_msgs__srv__MoveToJointTarget_Response
{
  bool success;
  rosidl_runtime_c__String message;
} gp7_task_executor_msgs__srv__MoveToJointTarget_Response;

// Struct for a sequence of gp7_task_executor_msgs__srv__MoveToJointTarget_Response.
typedef struct gp7_task_executor_msgs__srv__MoveToJointTarget_Response__Sequence
{
  gp7_task_executor_msgs__srv__MoveToJointTarget_Response * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} gp7_task_executor_msgs__srv__MoveToJointTarget_Response__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // GP7_TASK_EXECUTOR_MSGS__SRV__DETAIL__MOVE_TO_JOINT_TARGET__STRUCT_H_
