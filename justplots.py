import matplotlib.pyplot as plt
import numpy as np
from calculate import *

# use ggplot style for more sophisticated visuals
plt.style.use('ggplot')

def live_plotter_multi(x_vec,y1_data,y2_data, y3_data, y4_data, line1, line2, line3, line4, label, name, identifier='',pause_time=0.65):
    if line1==[]:
        # this is the call to matplotlib that allows dynamic plotting
        plt.ion()
        fig = plt.figure(2)
        ax = fig.add_subplot(111)
        # create a variable for the line so we can later update it
        line1, = ax.plot(x_vec,y1_data,'-o',alpha=0.8)  
        line2, = ax.plot(x_vec,y2_data,'-o',alpha=0.8)
        line3, = ax.plot(x_vec,y3_data,'-o',alpha=0.8)
        line4, = ax.plot(x_vec,y4_data,'-o',alpha=0.8)      
        #update plot label/title
        plt.legend([line1, line2, line3, line4],['Wind in X', 'Wind in Y', 'Wind in Z', 'Absolute Wind Speed'])
        plt.ylabel(label)
        plt.title(name.format(identifier))
        plt.show()
    
    # after the figure, axis, and line are created, we only need to update the y-data
    line1.set_ydata(y1_data)
    line2.set_ydata(y2_data)
    line3.set_ydata(y3_data)
    line4.set_ydata(y4_data)
    # adjust limits if new data goes beyond bounds
    if np.min(y1_data)<=line1.axes.get_ylim()[0] or np.max(y1_data)>=line1.axes.get_ylim()[1]:
        plt.ylim([np.min(y1_data)-np.std(y1_data),np.max(y1_data)+np.std(y1_data)])
    # this pauses the data so the figure/axis can catch up - the amount of pause can be altered above
    plt.pause(pause_time)
    
    # return line so we can update it again in the next iteration
    return [line1, line2, line3, line4]

if __name__ == "__main__":
    size = 5
    x_vec = np.linspace(0,1,size+1)[0:-1]
    #print(x_vec)
    y_vec1 = np.zeros(len(x_vec))
    y_vec2 = np.zeros(len(x_vec))
    y_vec3 = np.zeros(len(x_vec))
    y_vec4 = np.zeros(len(x_vec))
    #print(y_vec)
    line1 = []
    line2 = []
    line3 = []
    line4 = []

    wind_on = input("Do you want to see wind data? (y/n) \n")

    if wind_on == 'y':

        xlist = calc(0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)

        while True:
            try:
                
                xlist = calc(0, 0, 0, 0, 0, 0, 0, 0, xlist[6], xlist[7], xlist[8], xlist[9])

                y_vec1[-1] = xlist[6]
                y_vec2[-1] = xlist[7]
                y_vec3[-1] = xlist[8]
                y_vec4[-1] = xlist[9]

                [line1, line2, line3, line4] = live_plotter_multi(x_vec, y_vec1, y_vec2, y_vec3, y_vec4, line1, line2, line3, line4, 'Wind Speed (Knots)', 'Wind Velocity')
       
                y_vec1 = np.append(y_vec1[1:],0.0)
                y_vec2 = np.append(y_vec2[1:],0.0)
                y_vec3 = np.append(y_vec3[1:],0.0)
                y_vec4 = np.append(y_vec4[1:],0.0)

            except KeyboardInterrupt:
                back_on = input("You have paused. Continue? (y/n) \n")

                if back_on == 'y':
                    print("Continuing with program...\n")
                    continue

                elif back_on == 'n':
                    print("Halting Program...\n")
                    break

                else:
                    print("Invalid Selection\n")
                    print("Continuing with Program\n")
                    continue

    else:
        print("Goodbye\n")

