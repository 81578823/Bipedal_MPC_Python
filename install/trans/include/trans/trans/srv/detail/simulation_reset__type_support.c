// generated from rosidl_typesupport_introspection_c/resource/idl__type_support.c.em
// with input from trans:srv/SimulationReset.idl
// generated code does not contain a copyright notice

#include <stddef.h>
#include "trans/srv/detail/simulation_reset__rosidl_typesupport_introspection_c.h"
#include "trans/msg/rosidl_typesupport_introspection_c__visibility_control.h"
#include "rosidl_typesupport_introspection_c/field_types.h"
#include "rosidl_typesupport_introspection_c/identifier.h"
#include "rosidl_typesupport_introspection_c/message_introspection.h"
#include "trans/srv/detail/simulation_reset__functions.h"
#include "trans/srv/detail/simulation_reset__struct.h"


// Include directives for member types
// Member `header`
#include "std_msgs/msg/header.h"
// Member `header`
#include "std_msgs/msg/detail/header__rosidl_typesupport_introspection_c.h"
// Member `base_pose`
#include "geometry_msgs/msg/pose.h"
// Member `base_pose`
#include "geometry_msgs/msg/detail/pose__rosidl_typesupport_introspection_c.h"
// Member `joint_state`
#include "sensor_msgs/msg/joint_state.h"
// Member `joint_state`
#include "sensor_msgs/msg/detail/joint_state__rosidl_typesupport_introspection_c.h"

#ifdef __cplusplus
extern "C"
{
#endif

void trans__srv__SimulationReset_Request__rosidl_typesupport_introspection_c__SimulationReset_Request_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  trans__srv__SimulationReset_Request__init(message_memory);
}

void trans__srv__SimulationReset_Request__rosidl_typesupport_introspection_c__SimulationReset_Request_fini_function(void * message_memory)
{
  trans__srv__SimulationReset_Request__fini(message_memory);
}

static rosidl_typesupport_introspection_c__MessageMember trans__srv__SimulationReset_Request__rosidl_typesupport_introspection_c__SimulationReset_Request_message_member_array[3] = {
  {
    "header",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message (initialized later)
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(trans__srv__SimulationReset_Request, header),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "base_pose",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message (initialized later)
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(trans__srv__SimulationReset_Request, base_pose),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "joint_state",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message (initialized later)
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(trans__srv__SimulationReset_Request, joint_state),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers trans__srv__SimulationReset_Request__rosidl_typesupport_introspection_c__SimulationReset_Request_message_members = {
  "trans__srv",  // message namespace
  "SimulationReset_Request",  // message name
  3,  // number of fields
  sizeof(trans__srv__SimulationReset_Request),
  trans__srv__SimulationReset_Request__rosidl_typesupport_introspection_c__SimulationReset_Request_message_member_array,  // message members
  trans__srv__SimulationReset_Request__rosidl_typesupport_introspection_c__SimulationReset_Request_init_function,  // function to initialize message memory (memory has to be allocated)
  trans__srv__SimulationReset_Request__rosidl_typesupport_introspection_c__SimulationReset_Request_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t trans__srv__SimulationReset_Request__rosidl_typesupport_introspection_c__SimulationReset_Request_message_type_support_handle = {
  0,
  &trans__srv__SimulationReset_Request__rosidl_typesupport_introspection_c__SimulationReset_Request_message_members,
  get_message_typesupport_handle_function,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_trans
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, trans, srv, SimulationReset_Request)() {
  trans__srv__SimulationReset_Request__rosidl_typesupport_introspection_c__SimulationReset_Request_message_member_array[0].members_ =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, std_msgs, msg, Header)();
  trans__srv__SimulationReset_Request__rosidl_typesupport_introspection_c__SimulationReset_Request_message_member_array[1].members_ =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, geometry_msgs, msg, Pose)();
  trans__srv__SimulationReset_Request__rosidl_typesupport_introspection_c__SimulationReset_Request_message_member_array[2].members_ =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, sensor_msgs, msg, JointState)();
  if (!trans__srv__SimulationReset_Request__rosidl_typesupport_introspection_c__SimulationReset_Request_message_type_support_handle.typesupport_identifier) {
    trans__srv__SimulationReset_Request__rosidl_typesupport_introspection_c__SimulationReset_Request_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &trans__srv__SimulationReset_Request__rosidl_typesupport_introspection_c__SimulationReset_Request_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif

// already included above
// #include <stddef.h>
// already included above
// #include "trans/srv/detail/simulation_reset__rosidl_typesupport_introspection_c.h"
// already included above
// #include "trans/msg/rosidl_typesupport_introspection_c__visibility_control.h"
// already included above
// #include "rosidl_typesupport_introspection_c/field_types.h"
// already included above
// #include "rosidl_typesupport_introspection_c/identifier.h"
// already included above
// #include "rosidl_typesupport_introspection_c/message_introspection.h"
// already included above
// #include "trans/srv/detail/simulation_reset__functions.h"
// already included above
// #include "trans/srv/detail/simulation_reset__struct.h"


#ifdef __cplusplus
extern "C"
{
#endif

void trans__srv__SimulationReset_Response__rosidl_typesupport_introspection_c__SimulationReset_Response_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  trans__srv__SimulationReset_Response__init(message_memory);
}

void trans__srv__SimulationReset_Response__rosidl_typesupport_introspection_c__SimulationReset_Response_fini_function(void * message_memory)
{
  trans__srv__SimulationReset_Response__fini(message_memory);
}

static rosidl_typesupport_introspection_c__MessageMember trans__srv__SimulationReset_Response__rosidl_typesupport_introspection_c__SimulationReset_Response_message_member_array[1] = {
  {
    "is_success",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_BOOLEAN,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(trans__srv__SimulationReset_Response, is_success),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers trans__srv__SimulationReset_Response__rosidl_typesupport_introspection_c__SimulationReset_Response_message_members = {
  "trans__srv",  // message namespace
  "SimulationReset_Response",  // message name
  1,  // number of fields
  sizeof(trans__srv__SimulationReset_Response),
  trans__srv__SimulationReset_Response__rosidl_typesupport_introspection_c__SimulationReset_Response_message_member_array,  // message members
  trans__srv__SimulationReset_Response__rosidl_typesupport_introspection_c__SimulationReset_Response_init_function,  // function to initialize message memory (memory has to be allocated)
  trans__srv__SimulationReset_Response__rosidl_typesupport_introspection_c__SimulationReset_Response_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t trans__srv__SimulationReset_Response__rosidl_typesupport_introspection_c__SimulationReset_Response_message_type_support_handle = {
  0,
  &trans__srv__SimulationReset_Response__rosidl_typesupport_introspection_c__SimulationReset_Response_message_members,
  get_message_typesupport_handle_function,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_trans
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, trans, srv, SimulationReset_Response)() {
  if (!trans__srv__SimulationReset_Response__rosidl_typesupport_introspection_c__SimulationReset_Response_message_type_support_handle.typesupport_identifier) {
    trans__srv__SimulationReset_Response__rosidl_typesupport_introspection_c__SimulationReset_Response_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &trans__srv__SimulationReset_Response__rosidl_typesupport_introspection_c__SimulationReset_Response_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif

#include "rosidl_runtime_c/service_type_support_struct.h"
// already included above
// #include "trans/msg/rosidl_typesupport_introspection_c__visibility_control.h"
// already included above
// #include "trans/srv/detail/simulation_reset__rosidl_typesupport_introspection_c.h"
// already included above
// #include "rosidl_typesupport_introspection_c/identifier.h"
#include "rosidl_typesupport_introspection_c/service_introspection.h"

// this is intentionally not const to allow initialization later to prevent an initialization race
static rosidl_typesupport_introspection_c__ServiceMembers trans__srv__detail__simulation_reset__rosidl_typesupport_introspection_c__SimulationReset_service_members = {
  "trans__srv",  // service namespace
  "SimulationReset",  // service name
  // these two fields are initialized below on the first access
  NULL,  // request message
  // trans__srv__detail__simulation_reset__rosidl_typesupport_introspection_c__SimulationReset_Request_message_type_support_handle,
  NULL  // response message
  // trans__srv__detail__simulation_reset__rosidl_typesupport_introspection_c__SimulationReset_Response_message_type_support_handle
};

static rosidl_service_type_support_t trans__srv__detail__simulation_reset__rosidl_typesupport_introspection_c__SimulationReset_service_type_support_handle = {
  0,
  &trans__srv__detail__simulation_reset__rosidl_typesupport_introspection_c__SimulationReset_service_members,
  get_service_typesupport_handle_function,
};

// Forward declaration of request/response type support functions
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, trans, srv, SimulationReset_Request)();

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, trans, srv, SimulationReset_Response)();

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_trans
const rosidl_service_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_SYMBOL_NAME(rosidl_typesupport_introspection_c, trans, srv, SimulationReset)() {
  if (!trans__srv__detail__simulation_reset__rosidl_typesupport_introspection_c__SimulationReset_service_type_support_handle.typesupport_identifier) {
    trans__srv__detail__simulation_reset__rosidl_typesupport_introspection_c__SimulationReset_service_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  rosidl_typesupport_introspection_c__ServiceMembers * service_members =
    (rosidl_typesupport_introspection_c__ServiceMembers *)trans__srv__detail__simulation_reset__rosidl_typesupport_introspection_c__SimulationReset_service_type_support_handle.data;

  if (!service_members->request_members_) {
    service_members->request_members_ =
      (const rosidl_typesupport_introspection_c__MessageMembers *)
      ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, trans, srv, SimulationReset_Request)()->data;
  }
  if (!service_members->response_members_) {
    service_members->response_members_ =
      (const rosidl_typesupport_introspection_c__MessageMembers *)
      ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, trans, srv, SimulationReset_Response)()->data;
  }

  return &trans__srv__detail__simulation_reset__rosidl_typesupport_introspection_c__SimulationReset_service_type_support_handle;
}
