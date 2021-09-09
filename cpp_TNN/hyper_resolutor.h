#ifndef TNN_EXAMPLES_BASE_HYPER_RESOLUTOR_H_
#define TNN_EXAMPLES_BASE_HYPER_RESOLUTOR_H_

#include <algorithm>
#include <iostream>
#include <string>
#include <vector>

#include "tnn_sdk_sample.h"

namespace TNN_NS {

class ImageClassifierOutput : public TNNSDKOutput {
public:
    ImageClassifierOutput(std::shared_ptr<Mat> mat = nullptr) : TNNSDKOutput(mat) {};
    virtual ~HyperResolutorrOutput();
    
    int class_id = -1;
};

class HyperResolutor : public TNN_NS::TNNSDKSample {
public:
    virtual ~HyperResolutor();
    virtual MatConvertParam GetConvertParamForInput(std::string tag = "");
    virtual std::shared_ptr<TNNSDKOutput> CreateSDKOutput();
    virtual Status ProcessSDKOutput(std::shared_ptr<TNNSDKOutput> output);
    virtual std::shared_ptr<TNN_NS::Mat> ProcessSDKInputMat(std::shared_ptr<TNN_NS::Mat> mat,
                                                              std::string name);

};

}

#endif // TNN_EXAMPLES_BASE_IMAGE_CLASSIFIER_H_
