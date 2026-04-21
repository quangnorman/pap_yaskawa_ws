#[cfg(feature = "serde")]
use serde::{Deserialize, Serialize};



// Corresponds to gp7_vision_pipeline__msg__BoxDetection

// This struct is not documented.
#[allow(missing_docs)]

#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct BoxDetection {

    // This member is not documented.
    #[allow(missing_docs)]
    pub header: std_msgs::msg::Header,


    // This member is not documented.
    #[allow(missing_docs)]
    pub class_name: std::string::String,


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
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::msg::rmw::BoxDetection::default())
  }
}

impl rosidl_runtime_rs::Message for BoxDetection {
  type RmwMsg = super::msg::rmw::BoxDetection;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        header: std_msgs::msg::Header::into_rmw_message(std::borrow::Cow::Owned(msg.header)).into_owned(),
        class_name: msg.class_name.as_str().into(),
        confidence: msg.confidence,
        x_min: msg.x_min,
        y_min: msg.y_min,
        x_max: msg.x_max,
        y_max: msg.y_max,
        center_x: msg.center_x,
        center_y: msg.center_y,
        width_px: msg.width_px,
        height_px: msg.height_px,
        distance_m: msg.distance_m,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        header: std_msgs::msg::Header::into_rmw_message(std::borrow::Cow::Borrowed(&msg.header)).into_owned(),
        class_name: msg.class_name.as_str().into(),
      confidence: msg.confidence,
      x_min: msg.x_min,
      y_min: msg.y_min,
      x_max: msg.x_max,
      y_max: msg.y_max,
      center_x: msg.center_x,
      center_y: msg.center_y,
      width_px: msg.width_px,
      height_px: msg.height_px,
      distance_m: msg.distance_m,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      header: std_msgs::msg::Header::from_rmw_message(msg.header),
      class_name: msg.class_name.to_string(),
      confidence: msg.confidence,
      x_min: msg.x_min,
      y_min: msg.y_min,
      x_max: msg.x_max,
      y_max: msg.y_max,
      center_x: msg.center_x,
      center_y: msg.center_y,
      width_px: msg.width_px,
      height_px: msg.height_px,
      distance_m: msg.distance_m,
    }
  }
}


