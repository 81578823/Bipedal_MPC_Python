import pinocchio as pin        

rotation_matrix = pin.Quaternion(0.5, 0.5, 0.5, 0.5).matrix()

quat = pin.Quaternion()
quat = pin.Quaternion(rotation_matrix)

print(quat.coeffs())