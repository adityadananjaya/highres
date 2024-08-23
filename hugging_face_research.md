# Experimenting with the Hugging Face Models

## Selected Models:
**nielsr/detr-finetuned-boat-detection**
**zhuchi76/detr-resnet-50-finetuned-boat-dataset**
**wennnny/detr-resnet-50-finetuned-real-boat-dataset**
**leowang707/detr-resnet-50-finetuned-real-boat-dataset**
**facebook/detr-resnet-50**

## Image-dataset:
Running 16MP and the 64MP Woodford Bay images through each model

## Results:
### NIELSR
Was able to detect two boats on the 16MP image, no boats on the 64MP image (both images detected and identified an antenna 
as a boat).

### ZHUCHI76
Detected nothing

### WENNNNY
Detected nothing

### LEOWANG707
Detected nothing

### FACEBOOK
Detected almost all boats on the 16MP image and detected just a little less on the 64MP image (on the 16MP image detected
and identified an antenna)

## Conclusion:
Nielsr and Zhuchi76 were finetuned boat submodels of the facebook one (which is trained to find any object) yet despite the 
specialty, failed to procure decent results. Both Wennny and Leowang707 were also finetuned off of Zhuchi76 and also didn't
procure any results. 

The facebook model performed the best despite it not specialising in solely finding boats.

Any model that did procure any results performed better on the 16MP than the 64MP.