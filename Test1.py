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

    reward = 1.0

    if not all_wheels_on_track or is_offtrack:
        return 1e-3

    marker_1 = 0.1 * track_width
    marker_2 = 0.25 * track_width
    marker_3 = 0.5 * track_width

    if distance_from_center <= marker_1:
        reward += 2.0
    elif distance_from_center <= marker_2:
        reward += 1.0
    elif distance_from_center <= marker_3:
        reward += 0.5
    else:
        reward = 1e-3

    next_waypoint = waypoints[closest_waypoints[1]]
    prev_waypoint = waypoints[closest_waypoints[0]]
    
    track_direction = math.atan2(next_waypoint[1] - prev_waypoint[1], next_waypoint[0] - prev_waypoint[0])
    track_direction = math.degrees(track_direction)
    direction_diff = abs(track_direction - heading)

    if direction_diff < 10.0:
        SPEED_THRESHOLD = 1.00
    elif direction_diff < 20.0:
        SPEED_THRESHOLD = 0.67
    else:
        SPEED_THRESHOLD = 0.33

    if speed >= SPEED_THRESHOLD:
        reward += 2.0
    else:
        reward += 1.0 * (speed / SPEED_THRESHOLD)

    if steering_angle > 15.0 and speed == 1.00:
        reward *= 0.5

    if steering_angle < 15.0:
        reward += 0.5

    if steps > 0:
        progress_factor = progress / steps
        if progress_factor > 0.5:
            reward += 3.0 * progress_factor
        else:
            reward += 1.5 * progress_factor

    if progress == 100:
        if steps < 300:
            reward += 15.0
        else:
            reward += 10.0

    return float(reward)
