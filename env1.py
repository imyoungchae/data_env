import numpy as np
from isaacgym import gymapi, gymtorch, gymutil
import torch
import random

gym = gymapi.acquire_gym()

args = gymutil.parse_arguments(description="environment database", headless=True)

sim_params = gymapi.SimParams()
sim_params.dt = 1.0 / 60.0
sim_params.up_axis = gymapi.UP_AXIS_Z
sim_params.gravity = gymapi.Vec3(0.0, 0.0, -9.8)
if args.physics_engine == gymapi.SIM_FLEX:
    sim_params.flex.solver_type = 5
    sim_params.flex.num_outer_iterations = 4
    sim_params.flex.num_inner_iterations = 15
    sim_params.flex.relaxation = 0.75
    sim_params.flex.warm_start = 0.4
elif args.physics_engine == gymapi.SIM_PHYSX:
    sim_params.physx.solver_type = 1
    sim_params.physx.num_position_iterations = 4
    sim_params.physx.num_velocity_iterations = 1
    sim_params.physx.num_threads = args.num_threads
    sim_params.physx.use_gpu = args.use_gpu
    sim_params.physx.rest_offset = 0
    sim_params.physx.contact_offset = 0.001
    sim_params.physx.friction_offset_threshold = 0.001
    sim_params.physx.friction_correlation_distance = 0.0005

sim = gym.create_sim(args.compute_device_id, args.graphics_device_id, args.physics_engine, sim_params)

if sim is None:
    print("*** Failed to create sim")
    quit()

# create viewer
if not args.headless:
    viewer = gym.create_viewer(sim, gymapi.CameraProperties())
    if viewer is None:
        raise ValueError('*** Failed to create viewer')
    

# add ground plane with segmentation id zero
# so we can identify depths originating from the ground
# plane and ignore them
plane_params = gymapi.PlaneParams()
plane_params.normal = gymapi.Vec3(0.0, 0.0, 1.0)
plane_params.distance = 0.0
plane_params.static_friction = 1
plane_params.dynamic_friction = 1
plane_params.restitution = 0.0
plane_params.segmentation_id = 0
gym.add_ground(sim, plane_params)

gym.subscribe_viewer_keyboard_event(viewer, gymapi.KEY_V, "screenshot")

# Camera properties
cam_positions = []
cam_targets = []
cam_handles = []
cam_props = gymapi.CameraProperties()
cam_props.horizontal_fov = 70.0
cam_props.width = 1280
cam_props.height = 720


#cam_positions.append(gymapi.Vec3(1.0, 2.8, 1.5))
#cam_targets.append(gymapi.Vec3(3.0, 1.0, 0.8))
#cam_positions.append(gymapi.Vec3(1.5, 0.0, 3.0))
#cam_targets.append(gymapi.Vec3(1.5, 3.0, 0.5))


cam_positions.append(gymapi.Vec3(1.0, 1.0, 1.5))
cam_targets.append(gymapi.Vec3(3.0, 2.8, 0.8))

cam_positions.append(gymapi.Vec3(2.95, 1.7, 1.3))
cam_targets.append(gymapi.Vec3(1.5, 1.7, 0.4))

num_envs = 2
spacing = 15

env_lower = gymapi.Vec3(-spacing, 0.0, -spacing)
env_upper = gymapi.Vec3(spacing, spacing, spacing)

asset_root = "../../assets"

wall_options = gymapi.AssetOptions()
wall_options.fix_base_link = True
'''
wall_file = "urdf/wall.urdf"
wall_asset = gym.load_asset(sim, asset_root, wall_file, wall_options)
'''

wall_asset_1 = gym.create_box(sim,0.1,2.95,3.0,wall_options)
wall_asset_2 = gym.create_box(sim,3.0,0.1,3.0,wall_options)

table_options = gymapi.AssetOptions()
table_options.fix_base_link = True
#table_file="urdf/table.urdf"
#table_asset = gym.load_asset(sim, asset_root, table_file, table_options)

cube_file = "urdf/Room_Essentials_Fabric_Cube_Lavender/model.urdf"
cube_asset = gym.load_asset(sim, asset_root,cube_file, table_options)
basket_file = "urdf/Target_Basket_Medium/model.urdf"
basket_asset = gym.load_asset(sim, asset_root,basket_file, table_options)
ur5_file = "urdf/robot/ur_description/lk_ur5e_with_gripper.urdf"
asset_options = gymapi.AssetOptions()
ur5_asset = gym.load_asset(sim, asset_root,ur5_file, wall_options)
wall_options.default_dof_drive_mode = gymapi.DOF_MODE_POS

can_file = "urdf/ycb/002_master_chef_can/model.urdf"
can_asset = gym.load_asset(sim, asset_root,can_file, table_options)
cracker_file = "urdf/ycb/003_cracker_box/model.urdf"
cracker_asset = gym.load_asset(sim, asset_root,cracker_file, table_options)
sugar_file = "urdf/ycb/004_sugar_box/model.urdf"
sugar_asset = gym.load_asset(sim, asset_root,sugar_file, table_options)
tomato_file = "urdf/ycb/005_tomato_soup_can/model.urdf"
tomato_asset = gym.load_asset(sim, asset_root,tomato_file, table_options)
mustard_file = "urdf/ycb/006_mustard_bottle/model.urdf"
mustard_asset = gym.load_asset(sim, asset_root,mustard_file, table_options)

banana_file = "urdf/ycb/014_lemon/model.urdf"
banana_asset = gym.load_asset(sim, asset_root,banana_file, table_options)

plum_file = "urdf/ycb/011_banana/011_banana.urdf"
plum_asset = gym.load_asset(sim, asset_root,plum_file, table_options)

orange_file = "urdf/ycb/017_orange/model.urdf"
orange_asset = gym.load_asset(sim, asset_root,orange_file, table_options)

cooker_file = "urdf/google/TriStar_Products_PPC_Power_Pressure_Cooker_XL_in_Black/model.urdf"
cooker_asset = gym.load_asset(sim, asset_root, cooker_file, table_options)
knife_file = "urdf/google/JA_Henckels_International_Premio_Cutlery_Block_Set_14Piece/model.urdf"
knife_asset = gym.load_asset(sim, asset_root, knife_file, table_options)
frypan_file = "urdf/google/Chefmate_8_Frypan/model.urdf"
frypan_asset = gym.load_asset(sim, asset_root, frypan_file, table_options)
toast_file = "urdf/google/Black_and_Decker_TR3500SD_2Slice_Toaster/model.urdf"
toast_asset = gym.load_asset(sim, asset_root, toast_file, table_options)

drainer_file = "urdf/google/Rubbermaid_Large_Drainer/model.urdf"
drainer_asset = gym.load_asset(sim, asset_root, drainer_file, table_options)

sink_file = "urdf/google/KitchenCountertop/model.urdf"
sink_asset = gym.load_asset(sim, asset_root, sink_file, wall_options)
fridge_file = "urdf/google/Fridge/model.urdf"
fridge_asset = gym.load_asset(sim, asset_root, fridge_file, wall_options)
desk_file = "urdf/google/Desk/model.urdf"
desk_asset = gym.load_asset(sim, asset_root, desk_file, wall_options)

ur5_dof_props = gym.get_asset_dof_properties(ur5_asset)

for i in range(8):
    ur5_dof_props['stiffness'][i] = 1000
    ur5_dof_props['damping'][i] = 200
    ur5_dof_props['driveMode'][i] = gymapi.DOF_MODE_POS

asset_box = gym.create_box(sim,0.5,0.5,1.3,wall_options)

envs=[]

for i in range(num_envs):
    object_position = gymapi.Vec3(2.825,2.12,0.825)
    cam_handle = []
    env = gym.create_env(sim, env_lower, env_upper, 2)
    envs.append(env)

    wall1_actor = gym.create_actor(env, wall_asset_1,gymapi.Transform(p=gymapi.Vec3(0.0,1.475,1.5)),'wall1',i,0)
    wall2_actor = gym.create_actor(env, wall_asset_2,gymapi.Transform(p=gymapi.Vec3(1.5,3.0,1.5)),'wall2',i,0)
    wall3_actor = gym.create_actor(env, wall_asset_1,gymapi.Transform(p=gymapi.Vec3(3.0,1.475,1.5)),'wall3',i,0)
    '''gym.set_rigid_body_color(env,wall1_actor,0,gymapi.MESH_VISUAL_AND_COLLISION, gymapi.Vec3(0,0.2471,0.2784))
    gym.set_rigid_body_color(env,wall2_actor,0,gymapi.MESH_VISUAL_AND_COLLISION, gymapi.Vec3(0,0.2471,0.2784))
    gym.set_rigid_body_color(env,wall3_actor,0,gymapi.MESH_VISUAL_AND_COLLISION, gymapi.Vec3(0,0.2471,0.2784))
    gym.set_rigid_body_color(env,wall1_actor,0,gymapi.MESH_VISUAL_AND_COLLISION, gymapi.Vec3(0.9255,0.902,0.8))
    gym.set_rigid_body_color(env,wall2_actor,0,gymapi.MESH_VISUAL_AND_COLLISION, gymapi.Vec3(0.9255,0.902,0.8))
    gym.set_rigid_body_color(env,wall3_actor,0,gymapi.MESH_VISUAL_AND_COLLISION, gymapi.Vec3(0.9255,0.902,0.8))'''
   
    #table_actor = gym.create_actor(env, table_asset, gymapi.Transform(r=gymapi.Quat.from_axis_angle(gymapi.Vec3(0.0, 0.0, 1.0), np.pi/2) ,p=gymapi.Vec3(2.55,1.8,0.81)),'table',i,0)
    #basket_actor = gym.create_actor(env, basket_asset, gymapi.Transform(r=gymapi.Quat.from_axiis_angle(gymapi.Vec3(0.0, 0.0, 1.0), np.pi/2) ,p=gymapi.Vec3(2.55,1.5,0.2)),'basket',i,0)
    #gym.set_actor_scale(env, basket_actor, 2.0)
    ur5_actor = gym.create_actor(env, ur5_asset, gymapi.Transform(r=gymapi.Quat.from_axis_angle(gymapi.Vec3(0.0, 0.0, 1.0), -np.pi),p=gymapi.Vec3(1.5,2.5,0.9)),'ur5',i,0)
    gym.set_actor_dof_properties(env, ur5_actor, ur5_dof_props)
    box_actor=gym.create_actor(env, asset_box, gymapi.Transform(p=gymapi.Vec3(1.5,2.5,0.25)),'box',i,0)
    gym.set_rigid_body_color(env,box_actor,0,gymapi.MESH_VISUAL_AND_COLLISION, gymapi.Vec3(0,0.2471,0.5))
    sink_actor = gym.create_actor(env, sink_asset, gymapi.Transform(r=gymapi.Quat.from_axis_angle(gymapi.Vec3(0.0, 0.0, 1.0), np.pi/2),p=gymapi.Vec3(1.5,1.8,0.0)),'sink',i,0)
    #fridge_actor = gym.create_actor(env, fridge_asset, gymapi.Transform(r=gymapi.Quat.from_axis_angle(gymapi.Vec3(0.0, 0.0, 1.0), -np.pi/2),p=gymapi.Vec3(0.675,1.655,0.0)),'fridge',i,0)
    #fridge_actor = gym.create_actor(env, drainer_asset, gymapi.Transform(r=gymapi.Quat.from_axis_angle(gymapi.Vec3(0.0, 0.0, 1.0), -np.pi/2),p=gymapi.Vec3(2.7-1.125,0.8,1.2)),'fridge',i,0)
    '''desk_actor = gym.create_actor(env, desk_asset, gymapi.Transform(r=gymapi.Quat.from_axis_angle(gymapi.Vec3(0.0, 0.0, 1.0), np.pi/2),p=gymapi.Vec3(2.7-1.125,0.8,0.0)),'desk',i,0)
    gym.set_actor_scale(env, desk_actor, 1.5)
    deskcolor=gymapi.Vec3(0,0,0)
    gym.set_rigid_body_color(env,desk_actor, 0, gymapi.MESH_VISUAL, deskcolor)'''
    '''
    for k in range(8):
        cube_actor = gym.create_actor(env, cube_asset, gymapi.Transform(p=gymapi.Vec3(0.45+0.3*k,2.8,1.8)),'cube',i,0)
        #gym.set_rigid_body_color(env,cube_actor,0,gymapi.MESH_VISUAL_AND_COLLISION, gymapi.Vec3(random.random(), random.random(), random.random()))
    
    can_actor = gym.create_actor(env, can_asset, gymapi.Transform(p=object_position),'can', i, 0)
    object_position.y = object_position.y-0.15
    cracker_ator = gym.create_actor(env, cracker_asset, gymapi.Transform(p=object_position), 'cracker', i, 0)
    object_position.x = object_position.x-0.15
    object_position.y = object_position.y-0.2
    sugar_actor = gym.create_actor(env, sugar_asset, gymapi.Transform(p=object_position),'sugar', i, 0)
    object_position.x = object_position.x-0.15
    object_position.y = object_position.y-0.23
    tomato_actor = gym.create_actor(env, tomato_asset, gymapi.Transform(p=object_position), 'tomato', i, 0)
    object_position.y = object_position.y + 0.3
    mustard_actor = gym.create_actor(env, mustard_asset, gymapi.Transform(p=object_position),'mustard', i, 0)
    '''
    #drainer_actor = gym.create_actor(env, drainer_asset, gymapi.Transform(p=gymapi.Vec3(0.4,2.0,1.01)),'drainer', i, 0)
    cooker_actor = gym.create_actor(env,tomato_asset, gymapi.Transform(p=gymapi.Vec3(1.8,1.8,0.8),r=gymapi.Quat.from_axis_angle(gymapi.Vec3(0.0, 0.0, 1.0), -np.pi/2)),'cooker',i,0)
    object_position.y = object_position.y - 0.3
    object_position.x = object_position.x + 0.05
    toast_actor = gym.create_actor(env, toast_asset, gymapi.Transform(p=gymapi.Vec3(1.35,1.8,0.8),r=gymapi.Quat.from_axis_angle(gymapi.Vec3(0.0, 0.0, 1.0), -np.pi/2)), 'toast', i, 0)
    object_position.x = object_position.x - 0.5
    can_actor = gym.create_actor(env, frypan_asset, gymapi.Transform(p=gymapi.Vec3(1.60,1.8,0.8),r=gymapi.Quat.from_axis_angle(gymapi.Vec3(0.0, 0.0, 1.0), -np.pi/2)), 'can', i, 0)
    #camera
    wrist_body = gym.find_actor_rigid_body_handle(env,ur5_actor,"ee_link")
    for c in range(len(cam_positions)):
        cam_handle.append(gym.create_camera_sensor(env, cam_props))
        gym.set_camera_location(cam_handle[c], env, cam_positions[c], cam_targets[c])
    cam_handle.append(gym.create_camera_sensor(env, cam_props))
    local_transform = gymapi.Transform()
    local_transform.p = gymapi.Vec3(0.0, 0.0, -0.08)
    local_transform.r = gymapi.Quat.from_axis_angle(gymapi.Vec3(0.0, 1.0, 0.0), -np.pi/18) * gymapi.Quat.from_axis_angle(gymapi.Vec3(1.0, 0.0, 0.0), np.pi)
    gym.attach_camera_to_body(cam_handle[2], env, wrist_body, local_transform, gymapi.FOLLOW_TRANSFORM)
    cam_handles.append(cam_handle)
    l_color = gymapi.Vec3(0.8, 0.8, 0.8)
    l_ambient = gymapi.Vec3(0.8,0.8,0.8)
    l_direction = gymapi.Vec3(1.5,-1,10)
    gym.set_light_parameters(sim, 0, l_color, l_ambient, l_direction)
    #gym.set_light_parameters(sim, 0, gymapi.Vec3(), gymapi.Vec3(), gymapi.Vec3())
    gym.set_light_parameters(sim, 1, gymapi.Vec3(), gymapi.Vec3(), gymapi.Vec3())
    gym.set_light_parameters(sim, 2, gymapi.Vec3(), gymapi.Vec3(), gymapi.Vec3())

cam_pos = gymapi.Vec3(1.5, -1.5, 3.0)
cam_target = gymapi.Vec3(1.5, 3.0, 1.0)
gym.viewer_camera_look_at(viewer, envs[0], cam_pos, cam_target)
joint_positions = np.array([2.445,-1.0679, 1.2761, -2.0973,-1.6185,-1.5006,0.5000, 0.5000,-0.5000,-0.5000], dtype=np.float32)

while not gym.query_viewer_has_closed(viewer):
    gym.set_actor_dof_position_targets(envs[0], ur5_actor, joint_positions)
    # step the simulation
    gym.simulate(sim)
    gym.fetch_results(sim, True)
    gym.step_graphics(sim)
    gym.draw_viewer(viewer, sim, True)
    gym.sync_frame_time(sim)


gym.destroy_viewer(viewer)
gym.destroy_sim(sim)
