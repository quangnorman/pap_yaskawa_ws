// generated from rosidl_typesupport_introspection_c/resource/idl__type_support.c.em
// with input from gp7_task_executor_msgs:srv/MoveToPoseTarget.idl
// generated code does not contain a copyright notice

#include <stddef.h>
#include "gp7_task_executor_msgs/srv/detail/move_to_pose_target__rosidl_typesupport_introspection_c.h"
#include "gp7_task_executor_msgs/msg/rosidl_typesupport_introspection_c__visibility_control.h"
#include "rosidl_typesupport_introspection_c/field_types.h"
#include "rosidl_typesupport_introspection_c/identifier.h"
#include "rosidl_typesupport_introspection_c/message_introspection.h"
#include "gp7_task_executor_msgs/srv/detail/move_to_pose_target__functions.h"
#include "gp7_task_executor_msgs/srv/detail/move_to_pose_target__struct.h"


// Include directives for member types
// Member `pose`
#include "geometry_msgs/msg/pose.h"
// Member `pose`
#include "geometry_msgs/msg/detail/pose__rosidl_typesupport_introspection_c.h"
// Member `frame_id`
#include "rosidl_runtime_c/string_functions.h"

#ifdef __cplusplus
extern "C"
{
#endif

void gp7_task_executor_msgs__srv__MoveToPoseTarget_Request__rosidl_typesupport_introspection_c__MoveToPoseTarget_Request_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  gp7_task_executor_msgs__srv__MoveToPoseTarget_Request__init(message_memory);
}

void gp7_task_executor_msgs__srv__MoveToPoseTarget_Request__rosidl_typesupport_introspection_c__MoveToPoseTarget_Request_fini_function(void * message_memory)
{
  gp7_task_executor_msgs__srv__MoveToPoseTarget_Request__fini(message_memory);
}

static rosidl_typesupport_introspection_c__MessageMember gp7_task_executor_msgs__srv__MoveToPoseTarget_Request__rosidl_typesupport_introspection_c__MoveToPoseTarget_Request_message_member_array[3] = {
  {
    "pose",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message (initialized later)
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(gp7_task_executor_msgs__srv__MoveToPoseTarget_Request, pose),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "frame_id",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_STRING,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(gp7_task_executor_msgs__srv__MoveToPoseTarget_Request, frame_id),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "execute",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_BOOLEAN,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(gp7_task_executor_msgs__srv__MoveToPoseTarget_Request, execute),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers gp7_task_executor_msgs__srv__MoveToPoseTarget_Request__rosidl_typesupport_introspection_c__MoveToPoseTarget_Request_message_members = {
  "gp7_task_executor_msgs__srv",  // message namespace
  "MoveToPoseTarget_Request",  // message name
  3,  // number of fields
  sizeof(gp7_task_executor_msgs__srv__MoveToPoseTarget_Request),
  gp7_task_executor_msgs__srv__MoveToPoseTarget_Request__rosidl_typesupport_introspection_c__MoveToPoseTarget_Request_message_member_array,  // message members
  gp7_task_executor_msgs__srv__MoveToPoseTarget_Request__rosidl_typesupport_introspection_c__MoveToPoseTarget_Request_init_function,  // function to initialize message memory (memory has to be allocated)
  gp7_task_executor_msgs__srv__MoveToPoseTarget_Request__rosidl_typesupport_introspection_c__MoveToPoseTarget_Request_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t gp7_task_executor_msgs__srv__MoveToPoseTarget_Request__rosidl_typesupport_introspection_c__MoveToPoseTarget_Request_message_type_support_handle = {
  0,
  &gp7_task_executor_msgs__srv__MoveToPoseTarget_Request__rosidl_typesupport_introspection_c__MoveToPoseTarget_Request_message_members,
  get_message_typesupport_handle_function,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_gp7_task_executor_msgs
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, gp7_task_executor_msgs, srv, MoveToPoseTarget_Request)() {
  gp7_task_executor_msgs__srv__MoveToPoseTarget_Request__rosidl_typesupport_introspection_c__MoveToPoseTarget_Request_message_member_array[0].members_ =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, geometry_msgs, msg, Pose)();
  if (!gp7_task_executor_msgs__srv__MoveToPoseTarget_Request__rosidl_typesupport_introspection_c__MoveToPoseTarget_Request_message_type_support_handle.typesupport_identifier) {
    gp7_task_executor_msgs__srv__MoveToPoseTarget_Request__rosidl_typesupport_introspection_c__MoveToPoseTarget_Request_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &gp7_task_executor_msgs__srv__MoveToPoseTarget_Request__rosidl_typesupport_introspection_c__MoveToPoseTarget_Request_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif

// already included above
// #include <stddef.h>
// already included above
// #include "gp7_task_executor_msgs/srv/detail/move_to_pose_target__rosidl_typesupport_introspection_c.h"
// already included above
// #include "gp7_task_executor_msgs/msg/rosidl_typesupport_introspection_c__visibility_control.h"
// already included above
// #include "rosidl_typesupport_introspection_c/field_types.h"
// already included above
// #include "rosidl_typesupport_introspection_c/identifier.h"
// already included above
// #include "rosidl_typesupport_introspection_c/message_introspection.h"
// already included above
// #include "gp7_task_executor_msgs/srv/detail/move_to_pose_target__functions.h"
// already included above
// #include "gp7_task_executor_msgs/srv/detail/move_to_pose_target__struct.h"


// Include directives for member types
// Member `message`
// already included above
// #include "rosidl_runtime_c/string_functions.h"

#ifdef __cplusplus
extern "C"
{
#endif

void gp7_task_executor_msgs__srv__MoveToPoseTarget_Response__rosidl_typesupport_introspection_c__MoveToPoseTarget_Response_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  gp7_task_executor_msgs__srv__MoveToPoseTarget_Response__init(message_memory);
}

void gp7_task_executor_msgs__srv__MoveToPoseTarget_Response__rosidl_typesupport_introspection_c__MoveToPoseTarget_Response_fini_function(void * message_memory)
{
  gp7_task_executor_msgs__srv__MoveToPoseTarget_Response__fini(message_memory);
}

static rosidl_typesupport_introspection_c__MessageMember gp7_task_executor_msgs__srv__MoveToPoseTarget_Response__rosidl_typesupport_introspection_c__MoveToPoseTarget_Response_message_member_array[2] = {
  {
    "success",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_BOOLEAN,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(gp7_task_executor_msgs__srv__MoveToPoseTarget_Response, success),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "message",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_STRING,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(gp7_task_executor_msgs__srv__MoveToPoseTarget_Response, message),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers gp7_task_executor_msgs__srv__MoveToPoseTarget_Response__rosidl_typesupport_introspection_c__MoveToPoseTarget_Response_message_members = {
  "gp7_task_executor_msgs__srv",  // message namespace
  "MoveToPoseTarget_Response",  // message name
  2,  // number of fields
  sizeof(gp7_task_executor_msgs__srv__MoveToPoseTarget_Response),
  gp7_task_executor_msgs__srv__MoveToPoseTarget_Response__rosidl_typesupport_introspection_c__MoveToPoseTarget_Response_message_member_array,  // message members
  gp7_task_executor_msgs__srv__MoveToPoseTarget_Response__rosidl_typesupport_introspection_c__MoveToPoseTarget_Response_init_function,  // function to initialize message memory (memory has to be allocated)
  gp7_task_executor_msgs__srv__MoveToPoseTarget_Response__rosidl_typesupport_introspection_c__MoveToPoseTarget_Response_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t gp7_task_executor_msgs__srv__MoveToPoseTarget_Response__rosidl_typesupport_introspection_c__MoveToPoseTarget_Response_message_type_support_handle = {
  0,
  &gp7_task_executor_msgs__srv__MoveToPoseTarget_Response__rosidl_typesupport_introspection_c__MoveToPoseTarget_Response_message_members,
  get_message_typesupport_handle_function,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_gp7_task_executor_msgs
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, gp7_task_executor_msgs, srv, MoveToPoseTarget_Response)() {
  if (!gp7_task_executor_msgs__srv__MoveToPoseTarget_Response__rosidl_typesupport_introspection_c__MoveToPoseTarget_Response_message_type_support_handle.typesupport_identifier) {
    gp7_task_executor_msgs__srv__MoveToPoseTarget_Response__rosidl_typesupport_introspection_c__MoveToPoseTarget_Response_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &gp7_task_executor_msgs__srv__MoveToPoseTarget_Response__rosidl_typesupport_introspection_c__MoveToPoseTarget_Response_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif

#include "rosidl_runtime_c/service_type_support_struct.h"
// already included above
// #include "gp7_task_executor_msgs/msg/rosidl_typesupport_introspection_c__visibility_control.h"
// already included above
// #include "gp7_task_executor_msgs/srv/detail/move_to_pose_target__rosidl_typesupport_introspection_c.h"
// already included above
// #include "rosidl_typesupport_introspection_c/identifier.h"
#include "rosidl_typesupport_introspection_c/service_introspection.h"

// this is intentionally not const to allow initialization later to prevent an initialization race
static rosidl_typesupport_introspection_c__ServiceMembers gp7_task_executor_msgs__srv__detail__move_to_pose_target__rosidl_typesupport_introspection_c__MoveToPoseTarget_service_members = {
  "gp7_task_executor_msgs__srv",  // service namespace
  "MoveToPoseTarget",  // service name
  // these two fields are initialized below on the first access
  NULL,  // request message
  // gp7_task_executor_msgs__srv__detail__move_to_pose_target__rosidl_typesupport_introspection_c__MoveToPoseTarget_Request_message_type_support_handle,
  NULL  // response message
  // gp7_task_executor_msgs__srv__detail__move_to_pose_target__rosidl_typesupport_introspection_c__MoveToPoseTarget_Response_message_type_support_handle
};

static rosidl_service_type_support_t gp7_task_executor_msgs__srv__detail__move_to_pose_target__rosidl_typesupport_introspection_c__MoveToPoseTarget_service_type_support_handle = {
  0,
  &gp7_task_executor_msgs__srv__detail__move_to_pose_target__rosidl_typesupport_introspection_c__MoveToPoseTarget_service_members,
  get_service_typesupport_handle_function,
};

// Forward declaration of request/response type support functions
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, gp7_task_executor_msgs, srv, MoveToPoseTarget_Request)();

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, gp7_task_executor_msgs, srv, MoveToPoseTarget_Response)();

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_gp7_task_executor_msgs
const rosidl_service_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_SYMBOL_NAME(rosidl_typesupport_introspection_c, gp7_task_executor_msgs, srv, MoveToPoseTarget)() {
  if (!gp7_task_executor_msgs__srv__detail__move_to_pose_target__rosidl_typesupport_introspection_c__MoveToPoseTarget_service_type_support_handle.typesupport_identifier) {
    gp7_task_executor_msgs__srv__detail__move_to_pose_target__rosidl_typesupport_introspection_c__MoveToPoseTarget_service_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  rosidl_typesupport_introspection_c__ServiceMembers * service_members =
    (rosidl_typesupport_introspection_c__ServiceMembers *)gp7_task_executor_msgs__srv__detail__move_to_pose_target__rosidl_typesupport_introspection_c__MoveToPoseTarget_service_type_support_handle.data;

  if (!service_members->request_members_) {
    service_members->request_members_ =
      (const rosidl_typesupport_introspection_c__MessageMembers *)
      ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, gp7_task_executor_msgs, srv, MoveToPoseTarget_Request)()->data;
  }
  if (!service_members->response_members_) {
    service_members->response_members_ =
      (const rosidl_typesupport_introspection_c__MessageMembers *)
      ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, gp7_task_executor_msgs, srv, MoveToPoseTarget_Response)()->data;
  }

  return &gp7_task_executor_msgs__srv__detail__move_to_pose_target__rosidl_typesupport_introspection_c__MoveToPoseTarget_service_type_support_handle;
}
