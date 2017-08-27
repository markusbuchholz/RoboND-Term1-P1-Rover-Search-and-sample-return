import numpy as np


# This is where you can build a decision tree for determining throttle, brake and steer
# commands based on the output of the perception_step() function
def decision_step(Rover):

    # Implement conditionals to decide what to do given perception data
    # Here you're all set up with some basic functionality but you'll need to
    # improve on this decision tree to do a good job of navigating autonomously!


    if Rover.nav_angles is not None:
        # Check for Rover.mode status
        print (Rover.flag)
        if Rover.mode == 'forward':
            # Check the extent of navigable terrain
            if len(Rover.nav_angles) >= Rover.stop_forward:
                # If mode is forward, navigable terrain looks good
                # and velocity is below max, then throttle
                if Rover.vel < Rover.max_vel:
                    # Set throttle value to throttle setting
                    Rover.throttle = Rover.throttle_set

                else: # Else coast
                    Rover.throttle = 0
                Rover.brake = 0
                # Set steering to average angle clipped to the range +/- 15
                Rover.steer = np.clip(np.mean(Rover.nav_angles * 180/np.pi), -15, 15)
            # If there's a lack of navigable terrain pixels then go to 'stop' mode

            if (Rover.vel>0.05):
                print("reach")
                Rover.flag = True

            if (Rover.vel<0.001) and (Rover.throttle != 0):
                if Rover.flag == True:
                    #print("test")

                    Rover.throttle = 0
                    Rover.brake = Rover.brake_set_max
                    Rover.steer = -15
                    Rover.count += 1
                    #print ("counts", Rover.count)
                    if Rover.count > 5:

                        Rover.mode = 'forward'
                        Rover.count = 0
                        Rover.throttle = Rover.throttle_set
                        Rover.steer = np.clip(np.mean(Rover.nav_angles * 180/np.pi), -20, 20)
                        #print ("pic1", Rover.picking_up)
                else:
                    print("ACC")


            if Rover.picking_up:
                print ("picking up", Rover.picking_up)
                #print ("return")
                return Rover
            print("VELOCITY", Rover.vel)

            if len(Rover.rock_angles) > 1:
                print("Rock sample")
                if Rover.near_sample:
                    Rover.brake = Rover.brake_set_max
                    Rover.send_pickup = True
        # reduce the speed
                elif Rover.vel >= 0.85:
                    Rover.brake = Rover.brake_set_max
                elif Rover.vel < 0.85 and Rover.vel >= 0.45:
                    Rover.brake = 0
                    Rover.throttle = 0
                elif Rover.vel < 0.45:
                    Rover.brake = 0
                    Rover.throttle = Rover.throttle_set

                Rover.steer = np.clip(np.mean(Rover.rock_angles * 180 / np.pi), -20, 20)


            if len(Rover.nav_angles) < Rover.stop_forward:
                    # Set mode to "stop" and hit the brakes!
                    print("here")
                    Rover.throttle = 0
                    # Set brake to stored brake value
                    Rover.brake = Rover.brake_set
                    Rover.steer = 0
                    Rover.mode = 'stop'

            print ("END")

            if (Rover.vel<0.001) and (Rover.throttle != 0):
                if Rover.flag == True:
                    print("test")
                    #Rover.brake = 0
                    #Rover.brake = 0
                    Rover.throttle = 0
                    Rover.brake = 0

                    Rover.steer = -15
                    Rover.count += 1
                    #print ("counts", Rover.count)
                    if Rover.count > 5:

                        Rover.mode = 'forward'
                        Rover.count = 0

                        Rover.steer = np.clip(np.mean(Rover.nav_angles * 180/np.pi), -20, 20)
                        Rover.throttle = Rover.throttle_set

        # If we're already in "stop" mode then make different decisions
        elif Rover.mode == 'stop':
            Rover.flag = True # protect against rover looping

            # If we're in stop mode but still moving keep braking
            if Rover.vel > 0.2:
                Rover.throttle = 0
                Rover.brake = Rover.brake_set
                Rover.steer = 0
            # If we're not moving (vel < 0.2) then do something else
            elif Rover.vel <= 0.2:
                # Now we're stopped and we have vision data to see if there's a path forward
                if len(Rover.nav_angles) < Rover.go_forward:
                    Rover.throttle = 0
                    # Release the brake to allow turning
                    Rover.brake = 0
                    # Turn range is +/- 15 degrees, when stopped the next line will induce 4-wheel turning
                    Rover.steer = -15 # Could be more clever here about which way to turn
                # If we're stopped but see sufficient navigable terrain in front then go!
                if len(Rover.nav_angles) >= Rover.go_forward:
                    # Set throttle back to stored value
                    Rover.throttle = Rover.throttle_set
                    # Release the brake
                    Rover.brake = 0
                    # Set steer to mean angle
                    Rover.steer = np.clip(np.mean(Rover.nav_angles * 180/np.pi), -15, 15)
                    Rover.mode = 'forward'
                if (Rover.vel<0.001) and (Rover.throttle != 0):
                    print("test2")
                    Rover.brake = 0
                    Rover.throttle = 0

                    Rover.steer = -15
                    Rover.mode = 'forward'
                    Rover.throttle = Rover.throttle_set


    # Just to make the rover do something
    # even if no modifications have been made to the code
    else:
        Rover.throttle = Rover.throttle_set
        Rover.steer = 0
        Rover.brake = 0



    return Rover
