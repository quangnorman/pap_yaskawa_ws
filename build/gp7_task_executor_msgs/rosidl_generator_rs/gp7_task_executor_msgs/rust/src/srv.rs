#[cfg(feature = "serde")]
use serde::{Deserialize, Serialize};




// Corresponds to gp7_task_executor_msgs__srv__MoveToNamedTarget_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct MoveToNamedTarget_Request {

    // This member is not documented.
    #[allow(missing_docs)]
    pub target_name: std::string::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub execute: bool,

}



impl Default for MoveToNamedTarget_Request {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::MoveToNamedTarget_Request::default())
  }
}

impl rosidl_runtime_rs::Message for MoveToNamedTarget_Request {
  type RmwMsg = super::srv::rmw::MoveToNamedTarget_Request;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        target_name: msg.target_name.as_str().into(),
        execute: msg.execute,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        target_name: msg.target_name.as_str().into(),
      execute: msg.execute,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      target_name: msg.target_name.to_string(),
      execute: msg.execute,
    }
  }
}


// Corresponds to gp7_task_executor_msgs__srv__MoveToNamedTarget_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct MoveToNamedTarget_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub success: bool,


    // This member is not documented.
    #[allow(missing_docs)]
    pub message: std::string::String,

}



impl Default for MoveToNamedTarget_Response {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::MoveToNamedTarget_Response::default())
  }
}

impl rosidl_runtime_rs::Message for MoveToNamedTarget_Response {
  type RmwMsg = super::srv::rmw::MoveToNamedTarget_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        success: msg.success,
        message: msg.message.as_str().into(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      success: msg.success,
        message: msg.message.as_str().into(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      success: msg.success,
      message: msg.message.to_string(),
    }
  }
}


// Corresponds to gp7_task_executor_msgs__srv__MoveToJointTarget_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct MoveToJointTarget_Request {

    // This member is not documented.
    #[allow(missing_docs)]
    pub joint_names: Vec<std::string::String>,


    // This member is not documented.
    #[allow(missing_docs)]
    pub positions: Vec<f64>,


    // This member is not documented.
    #[allow(missing_docs)]
    pub execute: bool,

}



impl Default for MoveToJointTarget_Request {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::MoveToJointTarget_Request::default())
  }
}

impl rosidl_runtime_rs::Message for MoveToJointTarget_Request {
  type RmwMsg = super::srv::rmw::MoveToJointTarget_Request;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        joint_names: msg.joint_names
          .into_iter()
          .map(|elem| elem.as_str().into())
          .collect(),
        positions: msg.positions.into(),
        execute: msg.execute,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        joint_names: msg.joint_names
          .iter()
          .map(|elem| elem.as_str().into())
          .collect(),
        positions: msg.positions.as_slice().into(),
      execute: msg.execute,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      joint_names: msg.joint_names
          .into_iter()
          .map(|elem| elem.to_string())
          .collect(),
      positions: msg.positions
          .into_iter()
          .collect(),
      execute: msg.execute,
    }
  }
}


// Corresponds to gp7_task_executor_msgs__srv__MoveToJointTarget_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct MoveToJointTarget_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub success: bool,


    // This member is not documented.
    #[allow(missing_docs)]
    pub message: std::string::String,

}



impl Default for MoveToJointTarget_Response {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::MoveToJointTarget_Response::default())
  }
}

impl rosidl_runtime_rs::Message for MoveToJointTarget_Response {
  type RmwMsg = super::srv::rmw::MoveToJointTarget_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        success: msg.success,
        message: msg.message.as_str().into(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      success: msg.success,
        message: msg.message.as_str().into(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      success: msg.success,
      message: msg.message.to_string(),
    }
  }
}


// Corresponds to gp7_task_executor_msgs__srv__MoveToPoseTarget_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct MoveToPoseTarget_Request {

    // This member is not documented.
    #[allow(missing_docs)]
    pub pose: geometry_msgs::msg::Pose,


    // This member is not documented.
    #[allow(missing_docs)]
    pub frame_id: std::string::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub execute: bool,

}



impl Default for MoveToPoseTarget_Request {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::MoveToPoseTarget_Request::default())
  }
}

impl rosidl_runtime_rs::Message for MoveToPoseTarget_Request {
  type RmwMsg = super::srv::rmw::MoveToPoseTarget_Request;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        pose: geometry_msgs::msg::Pose::into_rmw_message(std::borrow::Cow::Owned(msg.pose)).into_owned(),
        frame_id: msg.frame_id.as_str().into(),
        execute: msg.execute,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        pose: geometry_msgs::msg::Pose::into_rmw_message(std::borrow::Cow::Borrowed(&msg.pose)).into_owned(),
        frame_id: msg.frame_id.as_str().into(),
      execute: msg.execute,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      pose: geometry_msgs::msg::Pose::from_rmw_message(msg.pose),
      frame_id: msg.frame_id.to_string(),
      execute: msg.execute,
    }
  }
}


// Corresponds to gp7_task_executor_msgs__srv__MoveToPoseTarget_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct MoveToPoseTarget_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub success: bool,


    // This member is not documented.
    #[allow(missing_docs)]
    pub message: std::string::String,

}



impl Default for MoveToPoseTarget_Response {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::MoveToPoseTarget_Response::default())
  }
}

impl rosidl_runtime_rs::Message for MoveToPoseTarget_Response {
  type RmwMsg = super::srv::rmw::MoveToPoseTarget_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        success: msg.success,
        message: msg.message.as_str().into(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      success: msg.success,
        message: msg.message.as_str().into(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      success: msg.success,
      message: msg.message.to_string(),
    }
  }
}


// Corresponds to gp7_task_executor_msgs__srv__MoveToNamedPoseTarget_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct MoveToNamedPoseTarget_Request {

    // This member is not documented.
    #[allow(missing_docs)]
    pub target_name: std::string::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub execute: bool,

}



impl Default for MoveToNamedPoseTarget_Request {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::MoveToNamedPoseTarget_Request::default())
  }
}

impl rosidl_runtime_rs::Message for MoveToNamedPoseTarget_Request {
  type RmwMsg = super::srv::rmw::MoveToNamedPoseTarget_Request;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        target_name: msg.target_name.as_str().into(),
        execute: msg.execute,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        target_name: msg.target_name.as_str().into(),
      execute: msg.execute,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      target_name: msg.target_name.to_string(),
      execute: msg.execute,
    }
  }
}


// Corresponds to gp7_task_executor_msgs__srv__MoveToNamedPoseTarget_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct MoveToNamedPoseTarget_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub success: bool,


    // This member is not documented.
    #[allow(missing_docs)]
    pub message: std::string::String,

}



impl Default for MoveToNamedPoseTarget_Response {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::MoveToNamedPoseTarget_Response::default())
  }
}

impl rosidl_runtime_rs::Message for MoveToNamedPoseTarget_Response {
  type RmwMsg = super::srv::rmw::MoveToNamedPoseTarget_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        success: msg.success,
        message: msg.message.as_str().into(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      success: msg.success,
        message: msg.message.as_str().into(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      success: msg.success,
      message: msg.message.to_string(),
    }
  }
}


// Corresponds to gp7_task_executor_msgs__srv__MoveToCartesianTarget_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
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
    pub frame_id: std::string::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub execute: bool,

}



impl Default for MoveToCartesianTarget_Request {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::MoveToCartesianTarget_Request::default())
  }
}

impl rosidl_runtime_rs::Message for MoveToCartesianTarget_Request {
  type RmwMsg = super::srv::rmw::MoveToCartesianTarget_Request;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        x: msg.x,
        y: msg.y,
        z: msg.z,
        frame_id: msg.frame_id.as_str().into(),
        execute: msg.execute,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      x: msg.x,
      y: msg.y,
      z: msg.z,
        frame_id: msg.frame_id.as_str().into(),
      execute: msg.execute,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      x: msg.x,
      y: msg.y,
      z: msg.z,
      frame_id: msg.frame_id.to_string(),
      execute: msg.execute,
    }
  }
}


// Corresponds to gp7_task_executor_msgs__srv__MoveToCartesianTarget_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct MoveToCartesianTarget_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub success: bool,


    // This member is not documented.
    #[allow(missing_docs)]
    pub message: std::string::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub fraction: f64,

}



impl Default for MoveToCartesianTarget_Response {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::MoveToCartesianTarget_Response::default())
  }
}

impl rosidl_runtime_rs::Message for MoveToCartesianTarget_Response {
  type RmwMsg = super::srv::rmw::MoveToCartesianTarget_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        success: msg.success,
        message: msg.message.as_str().into(),
        fraction: msg.fraction,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      success: msg.success,
        message: msg.message.as_str().into(),
      fraction: msg.fraction,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      success: msg.success,
      message: msg.message.to_string(),
      fraction: msg.fraction,
    }
  }
}


// Corresponds to gp7_task_executor_msgs__srv__MoveToNamedCartesianTarget_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct MoveToNamedCartesianTarget_Request {

    // This member is not documented.
    #[allow(missing_docs)]
    pub target_name: std::string::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub execute: bool,

}



impl Default for MoveToNamedCartesianTarget_Request {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::MoveToNamedCartesianTarget_Request::default())
  }
}

impl rosidl_runtime_rs::Message for MoveToNamedCartesianTarget_Request {
  type RmwMsg = super::srv::rmw::MoveToNamedCartesianTarget_Request;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        target_name: msg.target_name.as_str().into(),
        execute: msg.execute,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        target_name: msg.target_name.as_str().into(),
      execute: msg.execute,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      target_name: msg.target_name.to_string(),
      execute: msg.execute,
    }
  }
}


// Corresponds to gp7_task_executor_msgs__srv__MoveToNamedCartesianTarget_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct MoveToNamedCartesianTarget_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub success: bool,


    // This member is not documented.
    #[allow(missing_docs)]
    pub message: std::string::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub fraction: f64,

}



impl Default for MoveToNamedCartesianTarget_Response {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::MoveToNamedCartesianTarget_Response::default())
  }
}

impl rosidl_runtime_rs::Message for MoveToNamedCartesianTarget_Response {
  type RmwMsg = super::srv::rmw::MoveToNamedCartesianTarget_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        success: msg.success,
        message: msg.message.as_str().into(),
        fraction: msg.fraction,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      success: msg.success,
        message: msg.message.as_str().into(),
      fraction: msg.fraction,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      success: msg.success,
      message: msg.message.to_string(),
      fraction: msg.fraction,
    }
  }
}


// Corresponds to gp7_task_executor_msgs__srv__MoveCartesianSequence_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct MoveCartesianSequence_Request {

    // This member is not documented.
    #[allow(missing_docs)]
    pub waypoint_names: Vec<std::string::String>,


    // This member is not documented.
    #[allow(missing_docs)]
    pub execute: bool,

}



impl Default for MoveCartesianSequence_Request {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::MoveCartesianSequence_Request::default())
  }
}

impl rosidl_runtime_rs::Message for MoveCartesianSequence_Request {
  type RmwMsg = super::srv::rmw::MoveCartesianSequence_Request;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        waypoint_names: msg.waypoint_names
          .into_iter()
          .map(|elem| elem.as_str().into())
          .collect(),
        execute: msg.execute,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        waypoint_names: msg.waypoint_names
          .iter()
          .map(|elem| elem.as_str().into())
          .collect(),
      execute: msg.execute,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      waypoint_names: msg.waypoint_names
          .into_iter()
          .map(|elem| elem.to_string())
          .collect(),
      execute: msg.execute,
    }
  }
}


// Corresponds to gp7_task_executor_msgs__srv__MoveCartesianSequence_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct MoveCartesianSequence_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub success: bool,


    // This member is not documented.
    #[allow(missing_docs)]
    pub message: std::string::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub fraction: f64,

}



impl Default for MoveCartesianSequence_Response {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::MoveCartesianSequence_Response::default())
  }
}

impl rosidl_runtime_rs::Message for MoveCartesianSequence_Response {
  type RmwMsg = super::srv::rmw::MoveCartesianSequence_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        success: msg.success,
        message: msg.message.as_str().into(),
        fraction: msg.fraction,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      success: msg.success,
        message: msg.message.as_str().into(),
      fraction: msg.fraction,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      success: msg.success,
      message: msg.message.to_string(),
      fraction: msg.fraction,
    }
  }
}


// Corresponds to gp7_task_executor_msgs__srv__MoveSequence_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct MoveSequence_Request {

    // This member is not documented.
    #[allow(missing_docs)]
    pub waypoint_names: Vec<std::string::String>,


    // This member is not documented.
    #[allow(missing_docs)]
    pub execute: bool,

}



impl Default for MoveSequence_Request {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::MoveSequence_Request::default())
  }
}

impl rosidl_runtime_rs::Message for MoveSequence_Request {
  type RmwMsg = super::srv::rmw::MoveSequence_Request;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        waypoint_names: msg.waypoint_names
          .into_iter()
          .map(|elem| elem.as_str().into())
          .collect(),
        execute: msg.execute,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        waypoint_names: msg.waypoint_names
          .iter()
          .map(|elem| elem.as_str().into())
          .collect(),
      execute: msg.execute,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      waypoint_names: msg.waypoint_names
          .into_iter()
          .map(|elem| elem.to_string())
          .collect(),
      execute: msg.execute,
    }
  }
}


// Corresponds to gp7_task_executor_msgs__srv__MoveSequence_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct MoveSequence_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub success: bool,


    // This member is not documented.
    #[allow(missing_docs)]
    pub message: std::string::String,

}



impl Default for MoveSequence_Response {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::MoveSequence_Response::default())
  }
}

impl rosidl_runtime_rs::Message for MoveSequence_Response {
  type RmwMsg = super::srv::rmw::MoveSequence_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        success: msg.success,
        message: msg.message.as_str().into(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      success: msg.success,
        message: msg.message.as_str().into(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      success: msg.success,
      message: msg.message.to_string(),
    }
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


