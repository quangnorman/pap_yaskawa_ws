// generated from rosidl_typesupport_introspection_c/resource/idl__type_support.c.em
// with input from gp7_task_executor_msgs:srv/MoveToJointTarget.idl
// generated code does not contain a copyright notice

#include <stddef.h>
#include "gp7_task_executor_msgs/srv/detail/move_to_joint_target__rosidl_typesupport_introspection_c.h"
#include "gp7_task_executor_msgs/msg/rosidl_typesupport_introspection_c__visibility_control.h"
#include "rosidl_typesupport_introspection_c/field_types.h"
#include "rosidl_typesupport_introspection_c/identifier.h"
#include "rosidl_typesupport_introspection_c/message_introspection.h"
#include "gp7_task_executor_msgs/srv/detail/move_to_joint_target__functions.h"
#include "gp7_task_executor_msgs/srv/detail/move_to_joint_target__struct.h"


// Include directives for member types
// Member `joint_names`
#include "rosidl_runtime_c/string_functions.h"
// Member `positions`
#include "rosidl_runtime_c/primitives_sequence_functions.h"

#ifdef __cplusplus
extern "C"
{
#endif

void gp7_task_executor_msgs__srv__MoveToJointTarget_Request__rosidl_typesupport_introspection_c__MoveToJointTarget_Request_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  gp7_task_executor_msgs__srv__MoveToJointTarget_Request__init(message_memory);
}

void gp7_task_executor_msgs__srv__MoveToJointTarget_Request__rosidl_typesupport_introspection_c__MoveToJointTarget_Request_fini_function(void * message_memory)
{
  gp7_task_executor_msgs__srv__MoveToJointTarget_Request__fini(message_memory);
}

size_t gp7_task_executor_msgs__srv__MoveToJointTarget_Request__rosidl_typesupport_introspection_c__size_function__MoveToJointTarget_Request__joint_names(
  const void * untyped_member)
{
  const rosidl_runtime_c__String__Sequence * member =
    (const rosidl_runtime_c__String__Sequence *)(untyped_member);
  return member->size;
}

const void * gp7_task_executor_msgs__srv__MoveToJointTarget_Request__rosidl_typesupport_introspection_c__get_const_function__MoveToJointTarget_Request__joint_names(
  const void * untyped_member, size_t index)
{
  const rosidl_runtime_c__String__Sequence * member =
    (const rosidl_runtime_c__String__Sequence *)(untyped_member);
  return &member->data[index];
}

void * gp7_task_executor_msgs__srv__MoveToJointTarget_Request__rosidl_typesupport_introspection_c__get_function__MoveToJointTarget_Request__joint_names(
  void * untyped_member, size_t index)
{
  rosidl_runtime_c__String__Sequence * member =
    (rosidl_runtime_c__String__Sequence *)(untyped_member);
  return &member->data[index];
}

void gp7_task_executor_msgs__srv__MoveToJointTarget_Request__rosidl_typesupport_introspection_c__fetch_function__MoveToJointTarget_Request__joint_names(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const rosidl_runtime_c__String * item =
    ((const rosidl_runtime_c__String *)
    gp7_task_executor_msgs__srv__MoveToJointTarget_Request__rosidl_typesupport_introspection_c__get_const_function__MoveToJointTarget_Request__joint_names(untyped_member, index));
  rosidl_runtime_c__String * value =
    (rosidl_runtime_c__String *)(untyped_value);
  *value = *item;
}

void gp7_task_executor_msgs__srv__MoveToJointTarget_Request__rosidl_typesupport_introspection_c__assign_function__MoveToJointTarget_Request__joint_names(
  void * untyped_member, size_t index, const void * untyped_value)
{
  rosidl_runtime_c__String * item =
    ((rosidl_runtime_c__String *)
    gp7_task_executor_msgs__srv__MoveToJointTarget_Request__rosidl_typesupport_introspection_c__get_function__MoveToJointTarget_Request__joint_names(untyped_member, index));
  const rosidl_runtime_c__String * value =
    (const rosidl_runtime_c__String *)(untyped_value);
  *item = *value;
}

bool gp7_task_executor_msgs__srv__MoveToJointTarget_Request__rosidl_typesupport_introspection_c__resize_function__MoveToJointTarget_Request__joint_names(
  void * untyped_member, size_t size)
{
  rosidl_runtime_c__String__Sequence * member =
    (rosidl_runtime_c__String__Sequence *)(untyped_member);
  rosidl_runtime_c__String__Sequence__fini(member);
  return rosidl_runtime_c__String__Sequence__init(member, size);
}

size_t gp7_task_executor_msgs__srv__MoveToJointTarget_Request__rosidl_typesupport_introspection_c__size_function__MoveToJointTarget_Request__positions(
  const void * untyped_member)
{
  const rosidl_runtime_c__double__Sequence * member =
    (const rosidl_runtime_c__double__Sequence *)(untyped_member);
  return member->size;
}

const void * gp7_task_executor_msgs__srv__MoveToJointTarget_Request__rosidl_typesupport_introspection_c__get_const_function__MoveToJointTarget_Request__positions(
  const void * untyped_member, size_t index)
{
  const rosidl_runtime_c__double__Sequence * member =
    (const rosidl_runtime_c__double__Sequence *)(untyped_member);
  return &member->data[index];
}

void * gp7_task_executor_msgs__srv__MoveToJointTarget_Request__rosidl_typesupport_introspection_c__get_function__MoveToJointTarget_Request__positions(
  void * untyped_member, size_t index)
{
  rosidl_runtime_c__double__Sequence * member =
    (rosidl_runtime_c__double__Sequence *)(untyped_member);
  return &member->data[index];
}

void gp7_task_executor_msgs__srv__MoveToJointTarget_Request__rosidl_typesupport_introspection_c__fetch_function__MoveToJointTarget_Request__positions(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const double * item =
    ((const double *)
    gp7_task_executor_msgs__srv__MoveToJointTarget_Request__rosidl_typesupport_introspection_c__get_const_function__MoveToJointTarget_Request__positions(untyped_member, index));
  double * value =
    (double *)(untyped_value);
  *value = *item;
}

void gp7_task_executor_msgs__srv__MoveToJointTarget_Request__rosidl_typesupport_introspection_c__assign_function__MoveToJointTarget_Request__positions(
  void * untyped_member, size_t index, const void * untyped_value)
{
  double * item =
    ((double *)
    gp7_task_executor_msgs__srv__MoveToJointTarget_Request__rosidl_typesupport_introspection_c__get_function__MoveToJointTarget_Request__positions(untyped_member, index));
  const double * value =
    (const double *)(untyped_value);
  *item = *value;
}

bool gp7_task_executor_msgs__srv__MoveToJointTarget_Request__rosidl_typesupport_introspection_c__resize_function__MoveToJointTarget_Request__positions(
  void * untyped_member, size_t size)
{
  rosidl_runtime_c__double__Sequence * member =
    (rosidl_runtime_c__double__Sequence *)(untyped_member);
  rosidl_runtime_c__double__Sequence__fini(member);
  return rosidl_runtime_c__double__Sequence__init(member, size);
}

static rosidl_typesupport_introspection_c__MessageMember gp7_task_executor_msgs__srv__MoveToJointTarget_Request__rosidl_typesupport_introspection_c__MoveToJointTarget_Request_message_member_array[3] = {
  {
    "joint_names",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_STRING,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    true,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(gp7_task_executor_msgs__srv__MoveToJointTarget_Request, joint_names),  // bytes offset in struct
    NULL,  // default value
    gp7_task_executor_msgs__srv__MoveToJointTarget_Request__rosidl_typesupport_introspection_c__size_function__MoveToJointTarget_Request__joint_names,  // size() function pointer
    gp7_task_executor_msgs__srv__MoveToJointTarget_Request__rosidl_typesupport_introspection_c__get_const_function__MoveToJointTarget_Request__joint_names,  // get_const(index) function pointer
    gp7_task_executor_msgs__srv__MoveToJointTarget_Request__rosidl_typesupport_introspection_c__get_function__MoveToJointTarget_Request__joint_names,  // get(index) function pointer
    gp7_task_executor_msgs__srv__MoveToJointTarget_Request__rosidl_typesupport_introspection_c__fetch_function__MoveToJointTarget_Request__joint_names,  // fetch(index, &value) function pointer
    gp7_task_executor_msgs__srv__MoveToJointTarget_Request__rosidl_typesupport_introspection_c__assign_function__MoveToJointTarget_Request__joint_names,  // assign(index, value) function pointer
    gp7_task_executor_msgs__srv__MoveToJointTarget_Request__rosidl_typesupport_introspection_c__resize_function__MoveToJointTarget_Request__joint_names  // resize(index) function pointer
  },
  {
    "positions",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_DOUBLE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    true,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(gp7_task_executor_msgs__srv__MoveToJointTarget_Request, positions),  // bytes offset in struct
    NULL,  // default value
    gp7_task_executor_msgs__srv__MoveToJointTarget_Request__rosidl_typesupport_introspection_c__size_function__MoveToJointTarget_Request__positions,  // size() function pointer
    gp7_task_executor_msgs__srv__MoveToJointTarget_Request__rosidl_typesupport_introspection_c__get_const_function__MoveToJointTarget_Request__positions,  // get_const(index) function pointer
    gp7_task_executor_msgs__srv__MoveToJointTarget_Request__rosidl_typesupport_introspection_c__get_function__MoveToJointTarget_Request__positions,  // get(index) function pointer
    gp7_task_executor_msgs__srv__MoveToJointTarget_Request__rosidl_typesupport_introspection_c__fetch_function__MoveToJointTarget_Request__positions,  // fetch(index, &value) function pointer
    gp7_task_executor_msgs__srv__MoveToJointTarget_Request__rosidl_typesupport_introspection_c__assign_function__MoveToJointTarget_Request__positions,  // assign(index, value) function pointer
    gp7_task_executor_msgs__srv__MoveToJointTarget_Request__rosidl_typesupport_introspection_c__resize_function__MoveToJointTarget_Request__positions  // resize(index) function pointer
  },
  {
    "execute",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_BOOLEAN,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(gp7_task_executor_msgs__srv__MoveToJointTarget_Request, execute),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers gp7_task_executor_msgs__srv__MoveToJointTarget_Request__rosidl_typesupport_introspection_c__MoveToJointTarget_Request_message_members = {
  "gp7_task_executor_msgs__srv",  // message namespace
  "MoveToJointTarget_Request",  // message name
  3,  // number of fields
  sizeof(gp7_task_executor_msgs__srv__MoveToJointTarget_Request),
  gp7_task_executor_msgs__srv__MoveToJointTarget_Request__rosidl_typesupport_introspection_c__MoveToJointTarget_Request_message_member_array,  // message members
  gp7_task_executor_msgs__srv__MoveToJointTarget_Request__rosidl_typesupport_introspection_c__MoveToJointTarget_Request_init_function,  // function to initialize message memory (memory has to be allocated)
  gp7_task_executor_msgs__srv__MoveToJointTarget_Request__rosidl_typesupport_introspection_c__MoveToJointTarget_Request_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t gp7_task_executor_msgs__srv__MoveToJointTarget_Request__rosidl_typesupport_introspection_c__MoveToJointTarget_Request_message_type_support_handle = {
  0,
  &gp7_task_executor_msgs__srv__MoveToJointTarget_Request__rosidl_typesupport_introspection_c__MoveToJointTarget_Request_message_members,
  get_message_typesupport_handle_function,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_gp7_task_executor_msgs
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, gp7_task_executor_msgs, srv, MoveToJointTarget_Request)() {
  if (!gp7_task_executor_msgs__srv__MoveToJointTarget_Request__rosidl_typesupport_introspection_c__MoveToJointTarget_Request_message_type_support_handle.typesupport_identifier) {
    gp7_task_executor_msgs__srv__MoveToJointTarget_Request__rosidl_typesupport_introspection_c__MoveToJointTarget_Request_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &gp7_task_executor_msgs__srv__MoveToJointTarget_Request__rosidl_typesupport_introspection_c__MoveToJointTarget_Request_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif

// already included above
// #include <stddef.h>
// already included above
// #include "gp7_task_executor_msgs/srv/detail/move_to_joint_target__rosidl_typesupport_introspection_c.h"
// already included above
// #include "gp7_task_executor_msgs/msg/rosidl_typesupport_introspection_c__visibility_control.h"
// already included above
// #include "rosidl_typesupport_introspection_c/field_types.h"
// already included above
// #include "rosidl_typesupport_introspection_c/identifier.h"
// already included above
// #include "rosidl_typesupport_introspection_c/message_introspection.h"
// already included above
// #include "gp7_task_executor_msgs/srv/detail/move_to_joint_target__functions.h"
// already included above
// #include "gp7_task_executor_msgs/srv/detail/move_to_joint_target__struct.h"


// Include directives for member types
// Member `message`
// already included above
// #include "rosidl_runtime_c/string_functions.h"

#ifdef __cplusplus
extern "C"
{
#endif

void gp7_task_executor_msgs__srv__MoveToJointTarget_Response__rosidl_typesupport_introspection_c__MoveToJointTarget_Response_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  gp7_task_executor_msgs__srv__MoveToJointTarget_Response__init(message_memory);
}

void gp7_task_executor_msgs__srv__MoveToJointTarget_Response__rosidl_typesupport_introspection_c__MoveToJointTarget_Response_fini_function(void * message_memory)
{
  gp7_task_executor_msgs__srv__MoveToJointTarget_Response__fini(message_memory);
}

static rosidl_typesupport_introspection_c__MessageMember gp7_task_executor_msgs__srv__MoveToJointTarget_Response__rosidl_typesupport_introspection_c__MoveToJointTarget_Response_message_member_array[2] = {
  {
    "success",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_BOOLEAN,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(gp7_task_executor_msgs__srv__MoveToJointTarget_Response, success),  // bytes offset in struct
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
    offsetof(gp7_task_executor_msgs__srv__MoveToJointTarget_Response, message),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers gp7_task_executor_msgs__srv__MoveToJointTarget_Response__rosidl_typesupport_introspection_c__MoveToJointTarget_Response_message_members = {
  "gp7_task_executor_msgs__srv",  // message namespace
  "MoveToJointTarget_Response",  // message name
  2,  // number of fields
  sizeof(gp7_task_executor_msgs__srv__MoveToJointTarget_Response),
  gp7_task_executor_msgs__srv__MoveToJointTarget_Response__rosidl_typesupport_introspection_c__MoveToJointTarget_Response_message_member_array,  // message members
  gp7_task_executor_msgs__srv__MoveToJointTarget_Response__rosidl_typesupport_introspection_c__MoveToJointTarget_Response_init_function,  // function to initialize message memory (memory has to be allocated)
  gp7_task_executor_msgs__srv__MoveToJointTarget_Response__rosidl_typesupport_introspection_c__MoveToJointTarget_Response_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t gp7_task_executor_msgs__srv__MoveToJointTarget_Response__rosidl_typesupport_introspection_c__MoveToJointTarget_Response_message_type_support_handle = {
  0,
  &gp7_task_executor_msgs__srv__MoveToJointTarget_Response__rosidl_typesupport_introspection_c__MoveToJointTarget_Response_message_members,
  get_message_typesupport_handle_function,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_gp7_task_executor_msgs
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, gp7_task_executor_msgs, srv, MoveToJointTarget_Response)() {
  if (!gp7_task_executor_msgs__srv__MoveToJointTarget_Response__rosidl_typesupport_introspection_c__MoveToJointTarget_Response_message_type_support_handle.typesupport_identifier) {
    gp7_task_executor_msgs__srv__MoveToJointTarget_Response__rosidl_typesupport_introspection_c__MoveToJointTarget_Response_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &gp7_task_executor_msgs__srv__MoveToJointTarget_Response__rosidl_typesupport_introspection_c__MoveToJointTarget_Response_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif

#include "rosidl_runtime_c/service_type_support_struct.h"
// already included above
// #include "gp7_task_executor_msgs/msg/rosidl_typesupport_introspection_c__visibility_control.h"
// already included above
// #include "gp7_task_executor_msgs/srv/detail/move_to_joint_target__rosidl_typesupport_introspection_c.h"
// already included above
// #include "rosidl_typesupport_introspection_c/identifier.h"
#include "rosidl_typesupport_introspection_c/service_introspection.h"

// this is intentionally not const to allow initialization later to prevent an initialization race
static rosidl_typesupport_introspection_c__ServiceMembers gp7_task_executor_msgs__srv__detail__move_to_joint_target__rosidl_typesupport_introspection_c__MoveToJointTarget_service_members = {
  "gp7_task_executor_msgs__srv",  // service namespace
  "MoveToJointTarget",  // service name
  // these two fields are initialized below on the first access
  NULL,  // request message
  // gp7_task_executor_msgs__srv__detail__move_to_joint_target__rosidl_typesupport_introspection_c__MoveToJointTarget_Request_message_type_support_handle,
  NULL  // response message
  // gp7_task_executor_msgs__srv__detail__move_to_joint_target__rosidl_typesupport_introspection_c__MoveToJointTarget_Response_message_type_support_handle
};

static rosidl_service_type_support_t gp7_task_executor_msgs__srv__detail__move_to_joint_target__rosidl_typesupport_introspection_c__MoveToJointTarget_service_type_support_handle = {
  0,
  &gp7_task_executor_msgs__srv__detail__move_to_joint_target__rosidl_typesupport_introspection_c__MoveToJointTarget_service_members,
  get_service_typesupport_handle_function,
};

// Forward declaration of request/response type support functions
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, gp7_task_executor_msgs, srv, MoveToJointTarget_Request)();

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, gp7_task_executor_msgs, srv, MoveToJointTarget_Response)();

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_gp7_task_executor_msgs
const rosidl_service_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_SYMBOL_NAME(rosidl_typesupport_introspection_c, gp7_task_executor_msgs, srv, MoveToJointTarget)() {
  if (!gp7_task_executor_msgs__srv__detail__move_to_joint_target__rosidl_typesupport_introspection_c__MoveToJointTarget_service_type_support_handle.typesupport_identifier) {
    gp7_task_executor_msgs__srv__detail__move_to_joint_target__rosidl_typesupport_introspection_c__MoveToJointTarget_service_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  rosidl_typesupport_introspection_c__ServiceMembers * service_members =
    (rosidl_typesupport_introspection_c__ServiceMembers *)gp7_task_executor_msgs__srv__detail__move_to_joint_target__rosidl_typesupport_introspection_c__MoveToJointTarget_service_type_support_handle.data;

  if (!service_members->request_members_) {
    service_members->request_members_ =
      (const rosidl_typesupport_introspection_c__MessageMembers *)
      ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, gp7_task_executor_msgs, srv, MoveToJointTarget_Request)()->data;
  }
  if (!service_members->response_members_) {
    service_members->response_members_ =
      (const rosidl_typesupport_introspection_c__MessageMembers *)
      ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, gp7_task_executor_msgs, srv, MoveToJointTarget_Response)()->data;
  }

  return &gp7_task_executor_msgs__srv__detail__move_to_joint_target__rosidl_typesupport_introspection_c__MoveToJointTarget_service_type_support_handle;
}
