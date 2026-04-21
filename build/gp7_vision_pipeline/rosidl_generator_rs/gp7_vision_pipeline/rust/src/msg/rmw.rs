#[cfg(feature = "serde")]
use serde::{Deserialize, Serialize};


#[link(name = "gp7_vision_pipeline__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__gp7_vision_pipeline__msg__BoxDetection() -> *const std::ffi::c_void;
}

#[link(name = "gp7_vision_pipeline__rosidl_generator_c")]
extern "C" {
    fn gp7_vision_pipeline__msg__BoxDetection__init(msg: *mut BoxDetection) -> bool;
    fn gp7_vision_pipeline__msg__BoxDetection__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<BoxDetection>, size: usize) -> bool;
    fn gp7_vision_pipeline__msg__BoxDetection__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<BoxDetection>);
    fn gp7_vision_pipeline__msg__BoxDetection__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<BoxDetection>, out_seq: *mut rosidl_runtime_rs::Sequence<BoxDetection>) -> bool;
}

// Corresponds to gp7_vision_pipeline__msg__BoxDetection
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct BoxDetection {

    // This member is not documented.
    #[allow(missing_docs)]
    pub header: std_msgs::msg::rmw::Header,


    // This member is not documented.
    #[allow(missing_docs)]
    pub class_name: rosidl_runtime_rs::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub confidence: f32,


    // This member is not documented.
    #[allow(missing_docs)]
    pub x_min: i32,


    // This member is not documented.
    #[allow(missing_docs)]
    pub y_min: i32,


    // This member is not documented.
    #[allow(missing_docs)]
    pub x_max: i32,


    // This member is not documented.
    #[allow(missing_docs)]
    pub y_max: i32,


    // This member is not documented.
    #[allow(missing_docs)]
    pub center_x: i32,


    // This member is not documented.
    #[allow(missing_docs)]
    pub center_y: i32,


    // This member is not documented.
    #[allow(missing_docs)]
    pub width_px: i32,


    // This member is not documented.
    #[allow(missing_docs)]
    pub height_px: i32,


    // This member is not documented.
    #[allow(missing_docs)]
    pub distance_m: f32,

}



impl Default for BoxDetection {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !gp7_vision_pipeline__msg__BoxDetection__init(&mut msg as *mut _) {
        panic!("Call to gp7_vision_pipeline__msg__BoxDetection__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for BoxDetection {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { gp7_vision_pipeline__msg__BoxDetection__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { gp7_vision_pipeline__msg__BoxDetection__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { gp7_vision_pipeline__msg__BoxDetection__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for BoxDetection {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for BoxDetection where Self: Sized {
  const TYPE_NAME: &'static str = "gp7_vision_pipeline/msg/BoxDetection";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__gp7_vision_pipeline__msg__BoxDetection() }
  }
}


