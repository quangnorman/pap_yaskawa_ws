#[cfg(feature = "serde")]
use serde::{Deserialize, Serialize};



#[link(name = "gp7_task_executor_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__gp7_task_executor_msgs__srv__MoveToNamedTarget_Request() -> *const std::ffi::c_void;
}

#[link(name = "gp7_task_executor_msgs__rosidl_generator_c")]
extern "C" {
    fn gp7_task_executor_msgs__srv__MoveToNamedTarget_Request__init(msg: *mut MoveToNamedTarget_Request) -> bool;
    fn gp7_task_executor_msgs__srv__MoveToNamedTarget_Request__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<MoveToNamedTarget_Request>, size: usize) -> bool;
    fn gp7_task_executor_msgs__srv__MoveToNamedTarget_Request__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<MoveToNamedTarget_Request>);
    fn gp7_task_executor_msgs__srv__MoveToNamedTarget_Request__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<MoveToNamedTarget_Request>, out_seq: *mut rosidl_runtime_rs::Sequence<MoveToNamedTarget_Request>) -> bool;
}

// Corresponds to gp7_task_executor_msgs__srv__MoveToNamedTarget_Request
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct MoveToNamedTarget_Request {

    // This member is not documented.
    #[allow(missing_docs)]
    pub target_name: rosidl_runtime_rs::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub execute: bool,

}



impl Default for MoveToNamedTarget_Request {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !gp7_task_executor_msgs__srv__MoveToNamedTarget_Request__init(&mut msg as *mut _) {
        panic!("Call to gp7_task_executor_msgs__srv__MoveToNamedTarget_Request__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for MoveToNamedTarget_Request {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { gp7_task_executor_msgs__srv__MoveToNamedTarget_Request__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { gp7_task_executor_msgs__srv__MoveToNamedTarget_Request__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { gp7_task_executor_msgs__srv__MoveToNamedTarget_Request__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for MoveToNamedTarget_Request {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for MoveToNamedTarget_Request where Self: Sized {
  const TYPE_NAME: &'static str = "gp7_task_executor_msgs/srv/MoveToNamedTarget_Request";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__gp7_task_executor_msgs__srv__MoveToNamedTarget_Request() }
  }
}


#[link(name = "gp7_task_executor_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__gp7_task_executor_msgs__srv__MoveToNamedTarget_Response() -> *const std::ffi::c_void;
}

#[link(name = "gp7_task_executor_msgs__rosidl_generator_c")]
extern "C" {
    fn gp7_task_executor_msgs__srv__MoveToNamedTarget_Response__init(msg: *mut MoveToNamedTarget_Response) -> bool;
    fn gp7_task_executor_msgs__srv__MoveToNamedTarget_Response__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<MoveToNamedTarget_Response>, size: usize) -> bool;
    fn gp7_task_executor_msgs__srv__MoveToNamedTarget_Response__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<MoveToNamedTarget_Response>);
    fn gp7_task_executor_msgs__srv__MoveToNamedTarget_Response__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<MoveToNamedTarget_Response>, out_seq: *mut rosidl_runtime_rs::Sequence<MoveToNamedTarget_Response>) -> bool;
}

// Corresponds to gp7_task_executor_msgs__srv__MoveToNamedTarget_Response
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct MoveToNamedTarget_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub success: bool,


    // This member is not documented.
    #[allow(missing_docs)]
    pub message: rosidl_runtime_rs::String,

}



impl Default for MoveToNamedTarget_Response {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !gp7_task_executor_msgs__srv__MoveToNamedTarget_Response__init(&mut msg as *mut _) {
        panic!("Call to gp7_task_executor_msgs__srv__MoveToNamedTarget_Response__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for MoveToNamedTarget_Response {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { gp7_task_executor_msgs__srv__MoveToNamedTarget_Response__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { gp7_task_executor_msgs__srv__MoveToNamedTarget_Response__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { gp7_task_executor_msgs__srv__MoveToNamedTarget_Response__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for MoveToNamedTarget_Response {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for MoveToNamedTarget_Response where Self: Sized {
  const TYPE_NAME: &'static str = "gp7_task_executor_msgs/srv/MoveToNamedTarget_Response";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__gp7_task_executor_msgs__srv__MoveToNamedTarget_Response() }
  }
}


#[link(name = "gp7_task_executor_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__gp7_task_executor_msgs__srv__MoveToJointTarget_Request() -> *const std::ffi::c_void;
}

#[link(name = "gp7_task_executor_msgs__rosidl_generator_c")]
extern "C" {
    fn gp7_task_executor_msgs__srv__MoveToJointTarget_Request__init(msg: *mut MoveToJointTarget_Request) -> bool;
    fn gp7_task_executor_msgs__srv__MoveToJointTarget_Request__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<MoveToJointTarget_Request>, size: usize) -> bool;
    fn gp7_task_executor_msgs__srv__MoveToJointTarget_Request__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<MoveToJointTarget_Request>);
    fn gp7_task_executor_msgs__srv__MoveToJointTarget_Request__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<MoveToJointTarget_Request>, out_seq: *mut rosidl_runtime_rs::Sequence<MoveToJointTarget_Request>) -> bool;
}

// Corresponds to gp7_task_executor_msgs__srv__MoveToJointTarget_Request
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct MoveToJointTarget_Request {

    // This member is not documented.
    #[allow(missing_docs)]
    pub joint_names: rosidl_runtime_rs::Sequence<rosidl_runtime_rs::String>,


    // This member is not documented.
    #[allow(missing_docs)]
    pub positions: rosidl_runtime_rs::Sequence<f64>,


    // This member is not documented.
    #[allow(missing_docs)]
    pub execute: bool,

}



impl Default for MoveToJointTarget_Request {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !gp7_task_executor_msgs__srv__MoveToJointTarget_Request__init(&mut msg as *mut _) {
        panic!("Call to gp7_task_executor_msgs__srv__MoveToJointTarget_Request__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for MoveToJointTarget_Request {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { gp7_task_executor_msgs__srv__MoveToJointTarget_Request__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { gp7_task_executor_msgs__srv__MoveToJointTarget_Request__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { gp7_task_executor_msgs__srv__MoveToJointTarget_Request__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for MoveToJointTarget_Request {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for MoveToJointTarget_Request where Self: Sized {
  const TYPE_NAME: &'static str = "gp7_task_executor_msgs/srv/MoveToJointTarget_Request";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__gp7_task_executor_msgs__srv__MoveToJointTarget_Request() }
  }
}


#[link(name = "gp7_task_executor_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__gp7_task_executor_msgs__srv__MoveToJointTarget_Response() -> *const std::ffi::c_void;
}

#[link(name = "gp7_task_executor_msgs__rosidl_generator_c")]
extern "C" {
    fn gp7_task_executor_msgs__srv__MoveToJointTarget_Response__init(msg: *mut MoveToJointTarget_Response) -> bool;
    fn gp7_task_executor_msgs__srv__MoveToJointTarget_Response__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<MoveToJointTarget_Response>, size: usize) -> bool;
    fn gp7_task_executor_msgs__srv__MoveToJointTarget_Response__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<MoveToJointTarget_Response>);
    fn gp7_task_executor_msgs__srv__MoveToJointTarget_Response__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<MoveToJointTarget_Response>, out_seq: *mut rosidl_runtime_rs::Sequence<MoveToJointTarget_Response>) -> bool;
}

// Corresponds to gp7_task_executor_msgs__srv__MoveToJointTarget_Response
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct MoveToJointTarget_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub success: bool,


    // This member is not documented.
    #[allow(missing_docs)]
    pub message: rosidl_runtime_rs::String,

}



impl Default for MoveToJointTarget_Response {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !gp7_task_executor_msgs__srv__MoveToJointTarget_Response__init(&mut msg as *mut _) {
        panic!("Call to gp7_task_executor_msgs__srv__MoveToJointTarget_Response__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for MoveToJointTarget_Response {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { gp7_task_executor_msgs__srv__MoveToJointTarget_Response__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { gp7_task_executor_msgs__srv__MoveToJointTarget_Response__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { gp7_task_executor_msgs__srv__MoveToJointTarget_Response__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for MoveToJointTarget_Response {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for MoveToJointTarget_Response where Self: Sized {
  const TYPE_NAME: &'static str = "gp7_task_executor_msgs/srv/MoveToJointTarget_Response";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__gp7_task_executor_msgs__srv__MoveToJointTarget_Response() }
  }
}


#[link(name = "gp7_task_executor_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__gp7_task_executor_msgs__srv__MoveToPoseTarget_Request() -> *const std::ffi::c_void;
}

#[link(name = "gp7_task_executor_msgs__rosidl_generator_c")]
extern "C" {
    fn gp7_task_executor_msgs__srv__MoveToPoseTarget_Request__init(msg: *mut MoveToPoseTarget_Request) -> bool;
    fn gp7_task_executor_msgs__srv__MoveToPoseTarget_Request__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<MoveToPoseTarget_Request>, size: usize) -> bool;
    fn gp7_task_executor_msgs__srv__MoveToPoseTarget_Request__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<MoveToPoseTarget_Request>);
    fn gp7_task_executor_msgs__srv__MoveToPoseTarget_Request__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<MoveToPoseTarget_Request>, out_seq: *mut rosidl_runtime_rs::Sequence<MoveToPoseTarget_Request>) -> bool;
}

// Corresponds to gp7_task_executor_msgs__srv__MoveToPoseTarget_Request
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct MoveToPoseTarget_Request {

    // This member is not documented.
    #[allow(missing_docs)]
    pub pose: geometry_msgs::msg::rmw::Pose,


    // This member is not documented.
    #[allow(missing_docs)]
    pub frame_id: rosidl_runtime_rs::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub execute: bool,

}



impl Default for MoveToPoseTarget_Request {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !gp7_task_executor_msgs__srv__MoveToPoseTarget_Request__init(&mut msg as *mut _) {
        panic!("Call to gp7_task_executor_msgs__srv__MoveToPoseTarget_Request__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for MoveToPoseTarget_Request {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { gp7_task_executor_msgs__srv__MoveToPoseTarget_Request__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { gp7_task_executor_msgs__srv__MoveToPoseTarget_Request__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { gp7_task_executor_msgs__srv__MoveToPoseTarget_Request__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for MoveToPoseTarget_Request {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for MoveToPoseTarget_Request where Self: Sized {
  const TYPE_NAME: &'static str = "gp7_task_executor_msgs/srv/MoveToPoseTarget_Request";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__gp7_task_executor_msgs__srv__MoveToPoseTarget_Request() }
  }
}


#[link(name = "gp7_task_executor_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__gp7_task_executor_msgs__srv__MoveToPoseTarget_Response() -> *const std::ffi::c_void;
}

#[link(name = "gp7_task_executor_msgs__rosidl_generator_c")]
extern "C" {
    fn gp7_task_executor_msgs__srv__MoveToPoseTarget_Response__init(msg: *mut MoveToPoseTarget_Response) -> bool;
    fn gp7_task_executor_msgs__srv__MoveToPoseTarget_Response__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<MoveToPoseTarget_Response>, size: usize) -> bool;
    fn gp7_task_executor_msgs__srv__MoveToPoseTarget_Response__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<MoveToPoseTarget_Response>);
    fn gp7_task_executor_msgs__srv__MoveToPoseTarget_Response__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<MoveToPoseTarget_Response>, out_seq: *mut rosidl_runtime_rs::Sequence<MoveToPoseTarget_Response>) -> bool;
}

// Corresponds to gp7_task_executor_msgs__srv__MoveToPoseTarget_Response
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct MoveToPoseTarget_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub success: bool,


    // This member is not documented.
    #[allow(missing_docs)]
    pub message: rosidl_runtime_rs::String,

}



impl Default for MoveToPoseTarget_Response {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !gp7_task_executor_msgs__srv__MoveToPoseTarget_Response__init(&mut msg as *mut _) {
        panic!("Call to gp7_task_executor_msgs__srv__MoveToPoseTarget_Response__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for MoveToPoseTarget_Response {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { gp7_task_executor_msgs__srv__MoveToPoseTarget_Response__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { gp7_task_executor_msgs__srv__MoveToPoseTarget_Response__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { gp7_task_executor_msgs__srv__MoveToPoseTarget_Response__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for MoveToPoseTarget_Response {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for MoveToPoseTarget_Response where Self: Sized {
  const TYPE_NAME: &'static str = "gp7_task_executor_msgs/srv/MoveToPoseTarget_Response";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__gp7_task_executor_msgs__srv__MoveToPoseTarget_Response() }
  }
}


#[link(name = "gp7_task_executor_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__gp7_task_executor_msgs__srv__MoveToNamedPoseTarget_Request() -> *const std::ffi::c_void;
}

#[link(name = "gp7_task_executor_msgs__rosidl_generator_c")]
extern "C" {
    fn gp7_task_executor_msgs__srv__MoveToNamedPoseTarget_Request__init(msg: *mut MoveToNamedPoseTarget_Request) -> bool;
    fn gp7_task_executor_msgs__srv__MoveToNamedPoseTarget_Request__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<MoveToNamedPoseTarget_Request>, size: usize) -> bool;
    fn gp7_task_executor_msgs__srv__MoveToNamedPoseTarget_Request__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<MoveToNamedPoseTarget_Request>);
    fn gp7_task_executor_msgs__srv__MoveToNamedPoseTarget_Request__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<MoveToNamedPoseTarget_Request>, out_seq: *mut rosidl_runtime_rs::Sequence<MoveToNamedPoseTarget_Request>) -> bool;
}

// Corresponds to gp7_task_executor_msgs__srv__MoveToNamedPoseTarget_Request
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct MoveToNamedPoseTarget_Request {

    // This member is not documented.
    #[allow(missing_docs)]
    pub target_name: rosidl_runtime_rs::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub execute: bool,

}



impl Default for MoveToNamedPoseTarget_Request {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !gp7_task_executor_msgs__srv__MoveToNamedPoseTarget_Request__init(&mut msg as *mut _) {
        panic!("Call to gp7_task_executor_msgs__srv__MoveToNamedPoseTarget_Request__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for MoveToNamedPoseTarget_Request {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { gp7_task_executor_msgs__srv__MoveToNamedPoseTarget_Request__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { gp7_task_executor_msgs__srv__MoveToNamedPoseTarget_Request__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { gp7_task_executor_msgs__srv__MoveToNamedPoseTarget_Request__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for MoveToNamedPoseTarget_Request {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for MoveToNamedPoseTarget_Request where Self: Sized {
  const TYPE_NAME: &'static str = "gp7_task_executor_msgs/srv/MoveToNamedPoseTarget_Request";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__gp7_task_executor_msgs__srv__MoveToNamedPoseTarget_Request() }
  }
}


#[link(name = "gp7_task_executor_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__gp7_task_executor_msgs__srv__MoveToNamedPoseTarget_Response() -> *const std::ffi::c_void;
}

#[link(name = "gp7_task_executor_msgs__rosidl_generator_c")]
extern "C" {
    fn gp7_task_executor_msgs__srv__MoveToNamedPoseTarget_Response__init(msg: *mut MoveToNamedPoseTarget_Response) -> bool;
    fn gp7_task_executor_msgs__srv__MoveToNamedPoseTarget_Response__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<MoveToNamedPoseTarget_Response>, size: usize) -> bool;
    fn gp7_task_executor_msgs__srv__MoveToNamedPoseTarget_Response__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<MoveToNamedPoseTarget_Response>);
    fn gp7_task_executor_msgs__srv__MoveToNamedPoseTarget_Response__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<MoveToNamedPoseTarget_Response>, out_seq: *mut rosidl_runtime_rs::Sequence<MoveToNamedPoseTarget_Response>) -> bool;
}

// Corresponds to gp7_task_executor_msgs__srv__MoveToNamedPoseTarget_Response
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct MoveToNamedPoseTarget_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub success: bool,


    // This member is not documented.
    #[allow(missing_docs)]
    pub message: rosidl_runtime_rs::String,

}



impl Default for MoveToNamedPoseTarget_Response {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !gp7_task_executor_msgs__srv__MoveToNamedPoseTarget_Response__init(&mut msg as *mut _) {
        panic!("Call to gp7_task_executor_msgs__srv__MoveToNamedPoseTarget_Response__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for MoveToNamedPoseTarget_Response {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { gp7_task_executor_msgs__srv__MoveToNamedPoseTarget_Response__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { gp7_task_executor_msgs__srv__MoveToNamedPoseTarget_Response__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { gp7_task_executor_msgs__srv__MoveToNamedPoseTarget_Response__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for MoveToNamedPoseTarget_Response {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for MoveToNamedPoseTarget_Response where Self: Sized {
  const TYPE_NAME: &'static str = "gp7_task_executor_msgs/srv/MoveToNamedPoseTarget_Response";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__gp7_task_executor_msgs__srv__MoveToNamedPoseTarget_Response() }
  }
}


#[link(name = "gp7_task_executor_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__gp7_task_executor_msgs__srv__MoveToCartesianTarget_Request() -> *const std::ffi::c_void;
}

#[link(name = "gp7_task_executor_msgs__rosidl_generator_c")]
extern "C" {
    fn gp7_task_executor_msgs__srv__MoveToCartesianTarget_Request__init(msg: *mut MoveToCartesianTarget_Request) -> bool;
    fn gp7_task_executor_msgs__srv__MoveToCartesianTarget_Request__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<MoveToCartesianTarget_Request>, size: usize) -> bool;
    fn gp7_task_executor_msgs__srv__MoveToCartesianTarget_Request__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<MoveToCartesianTarget_Request>);
    fn gp7_task_executor_msgs__srv__MoveToCartesianTarget_Request__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<MoveToCartesianTarget_Request>, out_seq: *mut rosidl_runtime_rs::Sequence<MoveToCartesianTarget_Request>) -> bool;
}

// Corresponds to gp7_task_executor_msgs__srv__MoveToCartesianTarget_Request
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct MoveToCartesianTarget_Request {

    // This member is not documented.
    #[allow(missing_docs)]
    pub x: f64,


    // This member is not documented.
    #[allow(missing_docs)]
    pub y: f64,


    // This member is not documented.
    #[allow(missing_docs)]
    pub z: f64,


    // This member is not documented.
    #[allow(missing_docs)]
    pub frame_id: rosidl_runtime_rs::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub execute: bool,

}



impl Default for MoveToCartesianTarget_Request {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !gp7_task_executor_msgs__srv__MoveToCartesianTarget_Request__init(&mut msg as *mut _) {
        panic!("Call to gp7_task_executor_msgs__srv__MoveToCartesianTarget_Request__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for MoveToCartesianTarget_Request {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { gp7_task_executor_msgs__srv__MoveToCartesianTarget_Request__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { gp7_task_executor_msgs__srv__MoveToCartesianTarget_Request__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { gp7_task_executor_msgs__srv__MoveToCartesianTarget_Request__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for MoveToCartesianTarget_Request {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for MoveToCartesianTarget_Request where Self: Sized {
  const TYPE_NAME: &'static str = "gp7_task_executor_msgs/srv/MoveToCartesianTarget_Request";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__gp7_task_executor_msgs__srv__MoveToCartesianTarget_Request() }
  }
}


#[link(name = "gp7_task_executor_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__gp7_task_executor_msgs__srv__MoveToCartesianTarget_Response() -> *const std::ffi::c_void;
}

#[link(name = "gp7_task_executor_msgs__rosidl_generator_c")]
extern "C" {
    fn gp7_task_executor_msgs__srv__MoveToCartesianTarget_Response__init(msg: *mut MoveToCartesianTarget_Response) -> bool;
    fn gp7_task_executor_msgs__srv__MoveToCartesianTarget_Response__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<MoveToCartesianTarget_Response>, size: usize) -> bool;
    fn gp7_task_executor_msgs__srv__MoveToCartesianTarget_Response__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<MoveToCartesianTarget_Response>);
    fn gp7_task_executor_msgs__srv__MoveToCartesianTarget_Response__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<MoveToCartesianTarget_Response>, out_seq: *mut rosidl_runtime_rs::Sequence<MoveToCartesianTarget_Response>) -> bool;
}

// Corresponds to gp7_task_executor_msgs__srv__MoveToCartesianTarget_Response
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct MoveToCartesianTarget_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub success: bool,


    // This member is not documented.
    #[allow(missing_docs)]
    pub message: rosidl_runtime_rs::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub fraction: f64,

}



impl Default for MoveToCartesianTarget_Response {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !gp7_task_executor_msgs__srv__MoveToCartesianTarget_Response__init(&mut msg as *mut _) {
        panic!("Call to gp7_task_executor_msgs__srv__MoveToCartesianTarget_Response__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for MoveToCartesianTarget_Response {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { gp7_task_executor_msgs__srv__MoveToCartesianTarget_Response__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { gp7_task_executor_msgs__srv__MoveToCartesianTarget_Response__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { gp7_task_executor_msgs__srv__MoveToCartesianTarget_Response__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for MoveToCartesianTarget_Response {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for MoveToCartesianTarget_Response where Self: Sized {
  const TYPE_NAME: &'static str = "gp7_task_executor_msgs/srv/MoveToCartesianTarget_Response";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__gp7_task_executor_msgs__srv__MoveToCartesianTarget_Response() }
  }
}


#[link(name = "gp7_task_executor_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__gp7_task_executor_msgs__srv__MoveToNamedCartesianTarget_Request() -> *const std::ffi::c_void;
}

#[link(name = "gp7_task_executor_msgs__rosidl_generator_c")]
extern "C" {
    fn gp7_task_executor_msgs__srv__MoveToNamedCartesianTarget_Request__init(msg: *mut MoveToNamedCartesianTarget_Request) -> bool;
    fn gp7_task_executor_msgs__srv__MoveToNamedCartesianTarget_Request__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<MoveToNamedCartesianTarget_Request>, size: usize) -> bool;
    fn gp7_task_executor_msgs__srv__MoveToNamedCartesianTarget_Request__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<MoveToNamedCartesianTarget_Request>);
    fn gp7_task_executor_msgs__srv__MoveToNamedCartesianTarget_Request__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<MoveToNamedCartesianTarget_Request>, out_seq: *mut rosidl_runtime_rs::Sequence<MoveToNamedCartesianTarget_Request>) -> bool;
}

// Corresponds to gp7_task_executor_msgs__srv__MoveToNamedCartesianTarget_Request
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct MoveToNamedCartesianTarget_Request {

    // This member is not documented.
    #[allow(missing_docs)]
    pub target_name: rosidl_runtime_rs::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub execute: bool,

}



impl Default for MoveToNamedCartesianTarget_Request {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !gp7_task_executor_msgs__srv__MoveToNamedCartesianTarget_Request__init(&mut msg as *mut _) {
        panic!("Call to gp7_task_executor_msgs__srv__MoveToNamedCartesianTarget_Request__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for MoveToNamedCartesianTarget_Request {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { gp7_task_executor_msgs__srv__MoveToNamedCartesianTarget_Request__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { gp7_task_executor_msgs__srv__MoveToNamedCartesianTarget_Request__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { gp7_task_executor_msgs__srv__MoveToNamedCartesianTarget_Request__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for MoveToNamedCartesianTarget_Request {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for MoveToNamedCartesianTarget_Request where Self: Sized {
  const TYPE_NAME: &'static str = "gp7_task_executor_msgs/srv/MoveToNamedCartesianTarget_Request";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__gp7_task_executor_msgs__srv__MoveToNamedCartesianTarget_Request() }
  }
}


#[link(name = "gp7_task_executor_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__gp7_task_executor_msgs__srv__MoveToNamedCartesianTarget_Response() -> *const std::ffi::c_void;
}

#[link(name = "gp7_task_executor_msgs__rosidl_generator_c")]
extern "C" {
    fn gp7_task_executor_msgs__srv__MoveToNamedCartesianTarget_Response__init(msg: *mut MoveToNamedCartesianTarget_Response) -> bool;
    fn gp7_task_executor_msgs__srv__MoveToNamedCartesianTarget_Response__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<MoveToNamedCartesianTarget_Response>, size: usize) -> bool;
    fn gp7_task_executor_msgs__srv__MoveToNamedCartesianTarget_Response__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<MoveToNamedCartesianTarget_Response>);
    fn gp7_task_executor_msgs__srv__MoveToNamedCartesianTarget_Response__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<MoveToNamedCartesianTarget_Response>, out_seq: *mut rosidl_runtime_rs::Sequence<MoveToNamedCartesianTarget_Response>) -> bool;
}

// Corresponds to gp7_task_executor_msgs__srv__MoveToNamedCartesianTarget_Response
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct MoveToNamedCartesianTarget_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub success: bool,


    // This member is not documented.
    #[allow(missing_docs)]
    pub message: rosidl_runtime_rs::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub fraction: f64,

}



impl Default for MoveToNamedCartesianTarget_Response {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !gp7_task_executor_msgs__srv__MoveToNamedCartesianTarget_Response__init(&mut msg as *mut _) {
        panic!("Call to gp7_task_executor_msgs__srv__MoveToNamedCartesianTarget_Response__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for MoveToNamedCartesianTarget_Response {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { gp7_task_executor_msgs__srv__MoveToNamedCartesianTarget_Response__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { gp7_task_executor_msgs__srv__MoveToNamedCartesianTarget_Response__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { gp7_task_executor_msgs__srv__MoveToNamedCartesianTarget_Response__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for MoveToNamedCartesianTarget_Response {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for MoveToNamedCartesianTarget_Response where Self: Sized {
  const TYPE_NAME: &'static str = "gp7_task_executor_msgs/srv/MoveToNamedCartesianTarget_Response";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__gp7_task_executor_msgs__srv__MoveToNamedCartesianTarget_Response() }
  }
}


#[link(name = "gp7_task_executor_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__gp7_task_executor_msgs__srv__MoveCartesianSequence_Request() -> *const std::ffi::c_void;
}

#[link(name = "gp7_task_executor_msgs__rosidl_generator_c")]
extern "C" {
    fn gp7_task_executor_msgs__srv__MoveCartesianSequence_Request__init(msg: *mut MoveCartesianSequence_Request) -> bool;
    fn gp7_task_executor_msgs__srv__MoveCartesianSequence_Request__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<MoveCartesianSequence_Request>, size: usize) -> bool;
    fn gp7_task_executor_msgs__srv__MoveCartesianSequence_Request__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<MoveCartesianSequence_Request>);
    fn gp7_task_executor_msgs__srv__MoveCartesianSequence_Request__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<MoveCartesianSequence_Request>, out_seq: *mut rosidl_runtime_rs::Sequence<MoveCartesianSequence_Request>) -> bool;
}

// Corresponds to gp7_task_executor_msgs__srv__MoveCartesianSequence_Request
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct MoveCartesianSequence_Request {

    // This member is not documented.
    #[allow(missing_docs)]
    pub waypoint_names: rosidl_runtime_rs::Sequence<rosidl_runtime_rs::String>,


    // This member is not documented.
    #[allow(missing_docs)]
    pub execute: bool,

}



impl Default for MoveCartesianSequence_Request {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !gp7_task_executor_msgs__srv__MoveCartesianSequence_Request__init(&mut msg as *mut _) {
        panic!("Call to gp7_task_executor_msgs__srv__MoveCartesianSequence_Request__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for MoveCartesianSequence_Request {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { gp7_task_executor_msgs__srv__MoveCartesianSequence_Request__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { gp7_task_executor_msgs__srv__MoveCartesianSequence_Request__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { gp7_task_executor_msgs__srv__MoveCartesianSequence_Request__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for MoveCartesianSequence_Request {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for MoveCartesianSequence_Request where Self: Sized {
  const TYPE_NAME: &'static str = "gp7_task_executor_msgs/srv/MoveCartesianSequence_Request";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__gp7_task_executor_msgs__srv__MoveCartesianSequence_Request() }
  }
}


#[link(name = "gp7_task_executor_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__gp7_task_executor_msgs__srv__MoveCartesianSequence_Response() -> *const std::ffi::c_void;
}

#[link(name = "gp7_task_executor_msgs__rosidl_generator_c")]
extern "C" {
    fn gp7_task_executor_msgs__srv__MoveCartesianSequence_Response__init(msg: *mut MoveCartesianSequence_Response) -> bool;
    fn gp7_task_executor_msgs__srv__MoveCartesianSequence_Response__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<MoveCartesianSequence_Response>, size: usize) -> bool;
    fn gp7_task_executor_msgs__srv__MoveCartesianSequence_Response__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<MoveCartesianSequence_Response>);
    fn gp7_task_executor_msgs__srv__MoveCartesianSequence_Response__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<MoveCartesianSequence_Response>, out_seq: *mut rosidl_runtime_rs::Sequence<MoveCartesianSequence_Response>) -> bool;
}

// Corresponds to gp7_task_executor_msgs__srv__MoveCartesianSequence_Response
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct MoveCartesianSequence_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub success: bool,


    // This member is not documented.
    #[allow(missing_docs)]
    pub message: rosidl_runtime_rs::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub fraction: f64,

}



impl Default for MoveCartesianSequence_Response {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !gp7_task_executor_msgs__srv__MoveCartesianSequence_Response__init(&mut msg as *mut _) {
        panic!("Call to gp7_task_executor_msgs__srv__MoveCartesianSequence_Response__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for MoveCartesianSequence_Response {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { gp7_task_executor_msgs__srv__MoveCartesianSequence_Response__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { gp7_task_executor_msgs__srv__MoveCartesianSequence_Response__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { gp7_task_executor_msgs__srv__MoveCartesianSequence_Response__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for MoveCartesianSequence_Response {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for MoveCartesianSequence_Response where Self: Sized {
  const TYPE_NAME: &'static str = "gp7_task_executor_msgs/srv/MoveCartesianSequence_Response";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__gp7_task_executor_msgs__srv__MoveCartesianSequence_Response() }
  }
}


#[link(name = "gp7_task_executor_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__gp7_task_executor_msgs__srv__MoveSequence_Request() -> *const std::ffi::c_void;
}

#[link(name = "gp7_task_executor_msgs__rosidl_generator_c")]
extern "C" {
    fn gp7_task_executor_msgs__srv__MoveSequence_Request__init(msg: *mut MoveSequence_Request) -> bool;
    fn gp7_task_executor_msgs__srv__MoveSequence_Request__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<MoveSequence_Request>, size: usize) -> bool;
    fn gp7_task_executor_msgs__srv__MoveSequence_Request__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<MoveSequence_Request>);
    fn gp7_task_executor_msgs__srv__MoveSequence_Request__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<MoveSequence_Request>, out_seq: *mut rosidl_runtime_rs::Sequence<MoveSequence_Request>) -> bool;
}

// Corresponds to gp7_task_executor_msgs__srv__MoveSequence_Request
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct MoveSequence_Request {

    // This member is not documented.
    #[allow(missing_docs)]
    pub waypoint_names: rosidl_runtime_rs::Sequence<rosidl_runtime_rs::String>,


    // This member is not documented.
    #[allow(missing_docs)]
    pub execute: bool,

}



impl Default for MoveSequence_Request {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !gp7_task_executor_msgs__srv__MoveSequence_Request__init(&mut msg as *mut _) {
        panic!("Call to gp7_task_executor_msgs__srv__MoveSequence_Request__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for MoveSequence_Request {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { gp7_task_executor_msgs__srv__MoveSequence_Request__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { gp7_task_executor_msgs__srv__MoveSequence_Request__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { gp7_task_executor_msgs__srv__MoveSequence_Request__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for MoveSequence_Request {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for MoveSequence_Request where Self: Sized {
  const TYPE_NAME: &'static str = "gp7_task_executor_msgs/srv/MoveSequence_Request";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__gp7_task_executor_msgs__srv__MoveSequence_Request() }
  }
}


#[link(name = "gp7_task_executor_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__gp7_task_executor_msgs__srv__MoveSequence_Response() -> *const std::ffi::c_void;
}

#[link(name = "gp7_task_executor_msgs__rosidl_generator_c")]
extern "C" {
    fn gp7_task_executor_msgs__srv__MoveSequence_Response__init(msg: *mut MoveSequence_Response) -> bool;
    fn gp7_task_executor_msgs__srv__MoveSequence_Response__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<MoveSequence_Response>, size: usize) -> bool;
    fn gp7_task_executor_msgs__srv__MoveSequence_Response__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<MoveSequence_Response>);
    fn gp7_task_executor_msgs__srv__MoveSequence_Response__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<MoveSequence_Response>, out_seq: *mut rosidl_runtime_rs::Sequence<MoveSequence_Response>) -> bool;
}

// Corresponds to gp7_task_executor_msgs__srv__MoveSequence_Response
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct MoveSequence_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub success: bool,


    // This member is not documented.
    #[allow(missing_docs)]
    pub message: rosidl_runtime_rs::String,

}



impl Default for MoveSequence_Response {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !gp7_task_executor_msgs__srv__MoveSequence_Response__init(&mut msg as *mut _) {
        panic!("Call to gp7_task_executor_msgs__srv__MoveSequence_Response__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for MoveSequence_Response {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { gp7_task_executor_msgs__srv__MoveSequence_Response__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { gp7_task_executor_msgs__srv__MoveSequence_Response__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { gp7_task_executor_msgs__srv__MoveSequence_Response__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for MoveSequence_Response {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for MoveSequence_Response where Self: Sized {
  const TYPE_NAME: &'static str = "gp7_task_executor_msgs/srv/MoveSequence_Response";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__gp7_task_executor_msgs__srv__MoveSequence_Response() }
  }
}






#[link(name = "gp7_task_executor_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__gp7_task_executor_msgs__srv__MoveToNamedTarget() -> *const std::ffi::c_void;
}

// Corresponds to gp7_task_executor_msgs__srv__MoveToNamedTarget
#[allow(missing_docs, non_camel_case_types)]
pub struct MoveToNamedTarget;

impl rosidl_runtime_rs::Service for MoveToNamedTarget {
    type Request = MoveToNamedTarget_Request;
    type Response = MoveToNamedTarget_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__gp7_task_executor_msgs__srv__MoveToNamedTarget() }
    }
}




#[link(name = "gp7_task_executor_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__gp7_task_executor_msgs__srv__MoveToJointTarget() -> *const std::ffi::c_void;
}

// Corresponds to gp7_task_executor_msgs__srv__MoveToJointTarget
#[allow(missing_docs, non_camel_case_types)]
pub struct MoveToJointTarget;

impl rosidl_runtime_rs::Service for MoveToJointTarget {
    type Request = MoveToJointTarget_Request;
    type Response = MoveToJointTarget_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__gp7_task_executor_msgs__srv__MoveToJointTarget() }
    }
}




#[link(name = "gp7_task_executor_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__gp7_task_executor_msgs__srv__MoveToPoseTarget() -> *const std::ffi::c_void;
}

// Corresponds to gp7_task_executor_msgs__srv__MoveToPoseTarget
#[allow(missing_docs, non_camel_case_types)]
pub struct MoveToPoseTarget;

impl rosidl_runtime_rs::Service for MoveToPoseTarget {
    type Request = MoveToPoseTarget_Request;
    type Response = MoveToPoseTarget_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__gp7_task_executor_msgs__srv__MoveToPoseTarget() }
    }
}




#[link(name = "gp7_task_executor_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__gp7_task_executor_msgs__srv__MoveToNamedPoseTarget() -> *const std::ffi::c_void;
}

// Corresponds to gp7_task_executor_msgs__srv__MoveToNamedPoseTarget
#[allow(missing_docs, non_camel_case_types)]
pub struct MoveToNamedPoseTarget;

impl rosidl_runtime_rs::Service for MoveToNamedPoseTarget {
    type Request = MoveToNamedPoseTarget_Request;
    type Response = MoveToNamedPoseTarget_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__gp7_task_executor_msgs__srv__MoveToNamedPoseTarget() }
    }
}




#[link(name = "gp7_task_executor_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__gp7_task_executor_msgs__srv__MoveToCartesianTarget() -> *const std::ffi::c_void;
}

// Corresponds to gp7_task_executor_msgs__srv__MoveToCartesianTarget
#[allow(missing_docs, non_camel_case_types)]
pub struct MoveToCartesianTarget;

impl rosidl_runtime_rs::Service for MoveToCartesianTarget {
    type Request = MoveToCartesianTarget_Request;
    type Response = MoveToCartesianTarget_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__gp7_task_executor_msgs__srv__MoveToCartesianTarget() }
    }
}




#[link(name = "gp7_task_executor_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__gp7_task_executor_msgs__srv__MoveToNamedCartesianTarget() -> *const std::ffi::c_void;
}

// Corresponds to gp7_task_executor_msgs__srv__MoveToNamedCartesianTarget
#[allow(missing_docs, non_camel_case_types)]
pub struct MoveToNamedCartesianTarget;

impl rosidl_runtime_rs::Service for MoveToNamedCartesianTarget {
    type Request = MoveToNamedCartesianTarget_Request;
    type Response = MoveToNamedCartesianTarget_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__gp7_task_executor_msgs__srv__MoveToNamedCartesianTarget() }
    }
}




#[link(name = "gp7_task_executor_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__gp7_task_executor_msgs__srv__MoveCartesianSequence() -> *const std::ffi::c_void;
}

// Corresponds to gp7_task_executor_msgs__srv__MoveCartesianSequence
#[allow(missing_docs, non_camel_case_types)]
pub struct MoveCartesianSequence;

impl rosidl_runtime_rs::Service for MoveCartesianSequence {
    type Request = MoveCartesianSequence_Request;
    type Response = MoveCartesianSequence_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__gp7_task_executor_msgs__srv__MoveCartesianSequence() }
    }
}




#[link(name = "gp7_task_executor_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__gp7_task_executor_msgs__srv__MoveSequence() -> *const std::ffi::c_void;
}

// Corresponds to gp7_task_executor_msgs__srv__MoveSequence
#[allow(missing_docs, non_camel_case_types)]
pub struct MoveSequence;

impl rosidl_runtime_rs::Service for MoveSequence {
    type Request = MoveSequence_Request;
    type Response = MoveSequence_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__gp7_task_executor_msgs__srv__MoveSequence() }
    }
}


