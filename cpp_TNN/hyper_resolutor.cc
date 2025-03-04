#include "hyper_resolutor.h"
#include "sample_timer.h"
#include <cmath>

namespace TNN_NS {

HyperResolutorOutput::~HyperResolutorOutput() {}

HyperResolutor::~HyperResolutor() {}

std::shared_ptr<Mat> HyperResolutor::ProcessSDKInputMat(std::shared_ptr<Mat> input_mat,
                                                                   std::string name) {
    auto target_dims = GetInputShape(name);
    auto input_height = input_mat->GetHeight();
    auto input_width = input_mat->GetWidth();
    auto input_channel = input_mat->GetChannel();
    if (target_dims.size() >= 4 &&  input_channel == target_dims[1] &&
        (input_height != target_dims[2] || input_width != target_dims[3])) {
        auto target_mat = std::make_shared<TNN_NS::Mat>(input_mat->GetDeviceType(),
                                                        input_mat->GetMatType(), target_dims);
        auto status = Resize(input_mat, target_mat, TNNInterpLinear);
        if (status == TNN_OK) {
            return target_mat;
        } else {
            LOGE("%s\n", status.description().c_str());
            return nullptr;
        }
    }
  
    return input_mat;
}


MatConvertParam HyperResolutor::GetConvertParamForInput(std::string tag) {
    MatConvertParam input_cvt_param;
    input_cvt_param.scale = {1.0 / (255 * 0.229), 1.0 / (255 * 0.224), 1.0 / (255 * 0.225), 0.0}; 
    input_cvt_param.bias  = {-0.485 / 0.229, -0.456 / 0.224, -0.406 / 0.225, 0.0};
    return input_cvt_param;
}

std::shared_ptr<TNNSDKOutput> HyperResolutor::CreateSDKOutput() {
    return std::make_shared<HyperResolutorOutput>();
}

Status HyperResolutor::ProcessSDKOutput(std::shared_ptr<TNNSDKOutput> output_) {
    Status status = TNN_OK;
  
  
    auto output = dynamic_cast<HyperResolutorOutput *>(output_.get());
    RETURN_VALUE_ON_NEQ(!output, false,
                        Status(TNNERR_PARAM_ERR, "TNNSDKOutput is invalid"));
  
    
    auto output_mat_patch = output->GetMat();
    RETURN_VALUE_ON_NEQ(!output_mat_patch, false,
                        Status(TNNERR_PARAM_ERR, "output_mat_scores is invalid"));
    
    
    uint8_t *output_data_patch = (uint8_t*)output_mat_patch.get()->GetData(); 
  
  
    output->output_data_patch = output_data_patch;
  
    return status;
}

}
