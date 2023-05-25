load("yolov2_res18_6_3_2epoch.mat")

imgNode = ros2node("/tello_driver");
imgSub = ros2subscriber(imgNode,"image_raw");
pause(2)
imgMsg = receive(imgSub,10);
img = rosReadImage(imgMsg);
% displaydata = 0;
p1 = imshow(img);

while 1
    pause(0.01);
    imgMsg = receive(imgSub,10);
    img = rosReadImage(imgMsg);
    subImage = img(24:3:695, 32:4:927,:); %224x224x3 image
    
    [bboxes,scores,labels] = detect(detector,subImage);
    detectedI = insertObjectAnnotation(subImage,'Rectangle',bboxes,strcat(string(labels),{' - '},num2str(scores)));
    

    set(p1, 'CData', detectedI);

    %subImage = img(24:3:695, 32:4:927,:); %224x224x3 image
end