for i = 1:200
I = imread(testDataTbl.imageFilename{i});
[bboxes,scores,labels] = detect(detector,I);
detectedI = insertObjectAnnotation(I,'Rectangle',bboxes,cellstr(labels));
figure(gcf);
imshow(detectedI)
clf(fig)
end