import math

def reward_function(params):
    
    track_width = params['track_width']
    distance_from_center = params['distance_from_center']
    speed = params['speed']
    steering_angle = abs(params['steering_angle'])
    all_wheels_on_track = params['all_wheels_on_track']
    is_offtrack = params['is_offtrack']
    progress = params['progress']
    steps = params['steps']
    waypoints = params['waypoints']
    closest_waypoints = params['closest_waypoints']
    heading = params['heading']
    is_reversed = params['is_reversed']

    
    if not all_wheels_on_track or is_offtrack or is_reversed:
        return 1e-3  

    
    reward = 1.0

    
    marker_1 = 0.1 * track_width
    marker_2 = 0.25 * track_width
    marker_3 = 0.5 * track_width

    
    if distance_from_center <= marker_1:
        reward += 3.0
    elif distance_from_center <= marker_2:
        reward += 2.0
    elif distance_from_center <= marker_3:
        reward += 1.0
    else:
        return 1e-3  

    
    next_waypoint = waypoints[closest_waypoints[1]]
    prev_waypoint = waypoints[closest_waypoints[0]]
    
    track_direction = math.atan2(next_waypoint[1] - prev_waypoint[1], next_waypoint[0] - prev_waypoint[0])
    track_direction = math.degrees(track_direction)
    direction_diff = abs(track_direction - heading)
    
    if direction_diff > 180:
        direction_diff = 360 - direction_diff

    
    if direction_diff < 10.0:
        reward += 2.5
    elif direction_diff < 20.0:
        reward += 1.5
    else:
        reward *= 0.5  

    
    if direction_diff < 10.0:
        SPEED_THRESHOLD = 1.2  
    elif direction_diff < 20.0:
        SPEED_THRESHOLD = 0.8
    else:
        SPEED_THRESHOLD = 0.5

    
    if speed >= SPEED_THRESHOLD:
        reward += 2.0
    else:
        reward += 0.5 * (speed / SPEED_THRESHOLD)

    
    ABS_STEERING_THRESHOLD = 15.0 
    if steering_angle > ABS_STEERING_THRESHOLD and speed >= SPEED_THRESHOLD:
        reward *= 0.6  

    
    if steering_angle < ABS_STEERING_THRESHOLD:
        reward += 1.0

    
    progress_factor = progress / steps if steps > 0 else 0
    reward += 3.0 * progress_factor

    
    if progress == 100:
        if steps < 250:
            reward += 20.0
        else:
            reward += 10.0


    if (all_wheels_on_track and 
        distance_from_center < marker_1 and 
        speed >= SPEED_THRESHOLD and 
        direction_diff < 5.0):
        reward += 3.0 

    return float(reward)
