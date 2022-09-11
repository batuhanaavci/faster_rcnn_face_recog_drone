function out = jitterImageColorAndWarp(data)
% Unpack original data.
tabledan aldım augmente ettim tablea yazdım
[r, ~] = size(data);

for j = 1:r
    I = data{j,1};
    
    I = imread(cell2mat(I));
    figure(1);imshow(I);
    boxes = [];
    labels = [];
    for i = 2:8
        if sum(cell2mat(data{j,i}))>0
            if i == 2
            labels = [labels; cell('Batuhan')];
            boxes = [boxes; cell2mat(data{j,i})];
            end
            if i == 3
            labels = [labels; cell('Berkant')];
            boxes = [boxes; cell2mat(data{j,i})];
            end
            if i == 4
            labels = [labels; cell('Damla')];
            boxes = [boxes; cell2mat(data{j,i})];
            end
            if i == 5
            labels = [labels; cell('Enes')];
            boxes = [boxes; cell2mat(data{j,i})];
            end
            if i == 6
            labels = [labels; cell('Erdem')];
            boxes = [boxes; cell2mat(data{j,i})];
            end
            if i == 7
            labels = [labels; cell('Muhammed')];
            boxes = [boxes; cell2mat(data{j,i})];
            end
            if i == 8
            labels = [labels; cell('Omer')];
            boxes = [boxes; cell2mat(data{j,i})];
            end
    
        end
    end
    
    % Apply random color jitter.
    I = jitterColorHSV(I,"Contrast",0.4,"Saturation",0.2,'Hue',0.1);
    
    % Define random affine transform.ds
    tform = randomAffine2d("XReflection",true,'Rotation',[-30 30]);
    rout = affineOutputView(size(I),tform);
    
    % Transform image and bounding box labels.
    augmentedImage = imwarp(I,tform,"OutputView",rout);
    [augmentedBoxes, valid] = bboxwarp(boxes,tform,rout,'OverlapThreshold',0.4);
    augmentedLabels = labels;
    
    % Return augmented data.
    out = {augmentedImage,augmentedBoxes,augmentedLabels}
end
end

% 
% global files;
% folder = "frame/3/";
% files = dir(folder);,
% count = numel(files)-2;
% resizedFolder = "frame/resized_3/";
% 
% for frame=1:count
%     img = imread(folder+sprintf("%05d",frame)+".jpg");
%     subImage = img(24:3:695, 32:4:927,:);
%     imwrite(subImage,resizedFolder+sprintf("%05d",frame)+".jpg");
% end