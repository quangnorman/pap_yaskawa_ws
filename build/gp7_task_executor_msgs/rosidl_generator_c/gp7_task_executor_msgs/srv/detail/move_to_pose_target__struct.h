// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from gp7_task_executor_msgs:srv/MoveToPoseTarget.idl
// generated code does not contain a copyright notice

#ifndef GP7_TASK_EXECUTOR_MSGS__SRV__DETAIL__MOVE_TO_POSE_TARGET__STRUCT_H_
#define GP7_TASK_EXECUTOR_MSGS__SRV__DETAIL__MOVE_TO_POSE_TARGET__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

// Include directives for member types
// Member 'pose'
#include "geometry_msgs/msg/detail/pose__struct.h"
// Member 'frame_id'
#include "rosidl_runtime_c/string.h"

/// Struct defined in srv/MoveToPoseTarget in the package gp7_task_executor_msgs.
typedef struct gp7_task_executor_msgs__srv__MoveToPoseTarget_Request
{
  geometry_msgs__msg__Pose pose;
  rosidl_runtime_c__String frame_id;
  bool execute;
} gp7_task_executor_msgs__srv__MoveToPoseTarget_Request;

// Struct for a sequence of gp7_task_executor_msgs__srv__MoveToPoseTarget_Request.
typedef struct gp7_task_executor_msgs__srv__MoveToPoseTarget_Request__Sequence
{
  gp7_task_executor_msgs__srv__MoveToPoseTarget_Request * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} gp7_task_executor_msgs__srv__MoveToPoseTarget_Request__Sequence;


// Constants defined in the message

// Include directives for member types
// Member 'message'
// already included above
// #include "rosidl_runtime_c/string.h"

/// Struct defined in srv/MoveToPoseTarget in the package gp7_task_executor_msgs.
typedef struct gp7_task_executor_msgs__srv__MoveToPoseTarget_Response
{
  bool success;
  rosidl_runtime_c__String message;
} gp7_task_executor_msgs__srv__MoveToPoseTarget_Response;

// Struct for a sequence of gp7_task_executor_msgs__srv__MoveToPoseTarget_Response.
typedef struct gp7_task_executor_msgs__srv__MoveToPoseTarget_Response__Sequence
{
  gp7_task_executor_msgs__srv__MoveToPoseTarget_Response * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} gp7_task_executor_msgs__srv__MoveToPoseTarget_Response__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // GP7_TASK_EXECUTOR_MSGS__SRV__DETAIL__MOVE_TO_POSE_TARGET__STRUCT_H_
