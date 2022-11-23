clear
global files;
folder = "frame/3/";
files = dir(folder);
count = numel(files)-2;
disp(sprintf("%d",count)+" Frame Recorded");
%%
joyNode = ros2node("/joy_node");
joySub = ros2subscriber(joyNode,"/joy",@joyCallback);
imgNode = ros2node("/tello_driver");
imgSub = ros2subscriber(imgNode,"image_raw");
pause(2)
foldercount = 4;

global button;
global delaytime;
global state;
state = 1;
delaytime = 1;

frame = count-1;

while 1
    pause(delaytime);
    
    if state == 2
        disp(delaytime)
        imgMsg = receive(imgSub,10);
        img = rosReadImage(imgMsg);
        
        imwrite(img,folder+sprintf("%05d",frame)+".jpg");
        frame=frame+1;
        if frame >= 1000
            mkdir ("frame/", [int2str(foldercount)]);
            folder = ("frame/" + [int2str(foldercount)] + "/");
            files = dir(folder);
            count = numel(files)-2;
            foldercount = foldercount + 1;
            frame = count-1;

        end
    end
     
end

function joyCallback(joyData)
    global button;
    button1 = joyData.buttons(1); % joystick mavi buton : kaydi baslat
    button2 = joyData.buttons(2); % joystick yesil buton : kaydi durdur
    button3 = joyData.buttons(3); % joystick kirmizi buton : 0.1 sn'de bir foto kaydet
    button4 = joyData.buttons(4); % joystick sari buton : 1 sn'de bir foto kaydet
    global state;
    global delaytime;
    switch state
        case 1 %off 
            if button1 ==1
                clc;
                disp("Recording Started...")
                state =2;
            end
        case 2 %on           
            if button2 ==1
                clc;
                disp("Recording Stopped...")
                state = 1;
            end
    end
    if button3 == 1
        delaytime = 0.1;
    end
    if button4 == 1
        delaytime = 1;
    end
end