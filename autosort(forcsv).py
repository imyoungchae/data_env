import os
import pandas as pd

# Base directory containing numbered folders
base_dir = "/home/son/S_GLMS_L9_197"

# 필요한 열 목록 정의
required_columns = ['step', 'ee_pos_x', 'ee_pos_y', 'ee_pos_z', 'ee_rot_x', 'ee_rot_y',
       'ee_rot_z', 'ee_rot_w', 'robot_joint_pos_0', 'robot_joint_pos_1',
       'robot_joint_pos_2', 'robot_joint_pos_3', 'robot_joint_pos_4',
       'robot_joint_pos_5', 'robot_joint_pos_6', 'robot_joint_pos_7',
       'robot_joint_pos_8', 'robot_joint_pos_9', 'robot_joint_pos_10',
       'robot_joint_pos_11', 'ee_force_x', 'ee_force_y', 'ee_force_z',
       'ee_torque_x', 'ee_torque_y', 'ee_torque_z', 'contact_left_force_x',
       'contact_left_force_y', 'contact_left_force_z', 'contact_right_force_x',
       'contact_right_force_y', 'contact_right_force_z']

# Iterate over folders 0, 1, 2, 3, 4, 5
for i in range(6):
    folder_path = os.path.join(base_dir, str(i))
    input_file = os.path.join(folder_path, "data.csv")
    output_file = os.path.join(folder_path, "filtered_data.csv")
    
    if os.path.exists(input_file):
        # CSV 파일 읽기
        df = pd.read_csv(input_file)
        
        # 필요한 열만 선택
        df_filtered = df[required_columns]
        
        # Step 값이 6으로 나누어 떨어지는 행만 필터링
        df_filtered = df_filtered[df_filtered['step'] % 6 == 0]
        
        # Step 값을 0, 1, 2, 3...으로 순차적으로 재정의
        df_filtered['step'] = range(len(df_filtered))
        
        # 필터링된 데이터를 새로운 CSV 파일로 저장
        df_filtered.to_csv(output_file, index=False)
        
        print(f"Folder {i}: 필터링 및 재정렬된 CSV 파일이 '{output_file}'에 저장되었습니다.")
    else:
        print(f"Folder {i}: 'data.csv' 파일이 존재하지 않습니다.")
