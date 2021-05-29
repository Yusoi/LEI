
#include <oidn.hpp>
#include <oidn.h>
#include <exception>
#include <iostream>
#include <stdio.h>
#include <OpenImageIO\imageio.h>
#include <OpenImageIO\imagebuf.h>

// Our global image handles
OIIO::ImageBuf* input_colour = nullptr;
OIIO::ImageBuf* input_albedo = nullptr;
OIIO::ImageBuf* input_normal = nullptr;

void cleanup()
{
    if (input_colour) delete input_colour;
    if (input_albedo) delete input_albedo;
    if (input_normal) delete input_normal;
}

bool convertToFormat(void* in_ptr, void* out_ptr, unsigned int in_channels, unsigned int out_channels)
{
    switch (in_channels)
    {
    case(1):
    {
        switch (out_channels)
        {
        case(1):
        case(2):
        case(3):
        case(4): memcpy(out_ptr, in_ptr, sizeof(float)); return true;
        default: return false; // How has this happened?
        }
    }
    case(2):
    {
        switch (out_channels)
        {
        case(1): memcpy(out_ptr, in_ptr, sizeof(float)); return true;
        case(2):
        case(3):
        case(4): memcpy(out_ptr, in_ptr, 2 * sizeof(float)); return true;
        default: return false; // How has this happened?
        }
    }
    case(3):
    {
        switch (out_channels)
        {
        case(1): memcpy(out_ptr, in_ptr, 1 * sizeof(float)); return true;
        case(2): memcpy(out_ptr, in_ptr, 2 * sizeof(float)); return true;
        case(3):
        case(4): memcpy(out_ptr, in_ptr, 3 * sizeof(float)); return true;
        default: return false; // How has this happened?
        }
    }
    case(4):
    {
        switch (out_channels)
        {
        case(1): memcpy(out_ptr, in_ptr, 1 * sizeof(float)); return true;
        case(2): memcpy(out_ptr, in_ptr, 2 * sizeof(float)); return true;
        case(3): memcpy(out_ptr, in_ptr, 3 * sizeof(float)); return true;
        case(4): memcpy(out_ptr, in_ptr, 4 * sizeof(float)); return true;
        default: return false; // How has this happened?
        }
    }
    default: return false; // How has this happened?
    }
    return false; // some unsupported conversion
}

void errorCallback(void* userPtr, oidn::Error error, const char* message)
{
    throw std::runtime_error(message);
}

int main()
{
    bool c_loaded = false, n_loaded = false, a_loaded = false;
    std::string out_path;
    std::string in_path;

    input_colour = new OIIO::ImageBuf(in_path);
    if (input_colour->init_spec(in_path, 0, 0))
        c_loaded = true;
    else{
        cleanup();
        return -1;
    }

    input_normal = new OIIO::ImageBuf(in_path);
    if (input_normal->init_spec(in_path, 0, 0))
        c_loaded = true;
    else {
        cleanup();
        return -1;
    }

    input_albedo = new OIIO::ImageBuf(in_path);
    if (input_albedo->init_spec(in_path, 0, 0))
        c_loaded = true;
    else {
        cleanup();
        return -1;
    }

    // Check for a file extension
    int x = (int)out_path.find_last_of(".");
    x++;
    const char* ext_c = out_path.c_str() + x;
    std::string ext(ext_c);
    if (!ext.size())
    {
        std::cerr << "No output file extension";
        cleanup();
        return -1;
    }

    OIIO::ROI colour_roi, albedo_roi, normal_roi;
    colour_roi = OIIO::get_roi_full(input_colour->spec());
    int c_width = colour_roi.width();
    int c_height = colour_roi.height();
    if (a_loaded)
    {
        albedo_roi = OIIO::get_roi_full(input_albedo->spec());
        if (n_loaded)
            normal_roi = OIIO::get_roi_full(input_normal->spec());
    }

    // Check that our feature buffers are the same resolution as our colour
    int a_width = (a_loaded) ? albedo_roi.width() : 0;
    int a_height = (a_loaded) ? albedo_roi.height() : 0;
    if (a_loaded)
    {
        if (a_width != c_width || a_height != c_height)
        {
            std::cerr << "Aldedo image not same resolution as colour";
            cleanup();
            return -1;
        }
    }

    int n_width = (n_loaded) ? normal_roi.width() : 0;
    int n_height = (n_loaded) ? normal_roi.height() : 0;
    if (n_loaded)
    {
        if (n_width != c_width || n_height != c_height)
        {
            std::cerr << "Normal image not same resolution as colour";
            cleanup();
            return -1;
        }
    }

    // Create our output buffer
    std::vector<float> output_pixels(c_width * c_height * 3);

    // Get our pixel data
    std::vector<float> colour_pixels(c_width * c_height * colour_roi.nchannels());
    input_colour->get_pixels(colour_roi, OIIO::TypeDesc::FLOAT, &colour_pixels[0]);
    std::vector<float> colour_pixels_float3(c_width * c_height * 3);
    // Convert buffer to float3
    float* in = (float*)colour_pixels.data();
    float* out = (float*)colour_pixels_float3.data();
    for (unsigned int i = 0; i < colour_pixels.size(); i += colour_roi.nchannels())
    {
        if (!convertToFormat(in, out, colour_roi.nchannels(), 3))
        {
            std::cerr << "Failed to convert colour to float3";
            cleanup();
            return -1;
        }
        in += colour_roi.nchannels();
        out += 3;
    }


    std::vector<float> albedo_pixels;
    if (a_loaded)
    {
        std::vector<float> albedo_pixels_temp(a_width * a_height * albedo_roi.nchannels());
        input_albedo->get_pixels(albedo_roi, OIIO::TypeDesc::FLOAT, &albedo_pixels_temp[0]);
        albedo_pixels.resize(a_width * a_height * 3);
        in = (float*)albedo_pixels_temp.data();
        out = (float*)albedo_pixels.data();
        // Convert buffer to float3
        for (unsigned int i = 0; i < albedo_pixels_temp.size(); i += albedo_roi.nchannels())
        {
            if (!convertToFormat(in, out, albedo_roi.nchannels(), 3))
            {
                std::cerr << "Failed to convert albedo to float3";
                cleanup();
                return -1;
            }
            in += albedo_roi.nchannels();
            out += 3;
        }
    }

    std::vector<float> normal_pixels;
    if (n_loaded)
    {
        std::vector<float> normal_pixels_temp(n_width * n_height * normal_roi.nchannels());
        input_normal->get_pixels(normal_roi, OIIO::TypeDesc::FLOAT, &normal_pixels_temp[0]);
        normal_pixels.resize(n_width * n_height * 3);
        in = (float*)normal_pixels_temp.data();
        out = (float*)normal_pixels.data();
        // Convert buffer to float3
        for (unsigned int i = 0; i < normal_pixels_temp.size(); i += normal_roi.nchannels())
        {
            if (!convertToFormat(in, out, normal_roi.nchannels(), 3))
            {
                std::cerr << "Failed to convert normal to float3";
                cleanup();
                return -1;
            }
            in += normal_roi.nchannels();
            out += 3;
        }
    }

    // Catch exceptions
    try
    {
        // Create our device
        oidn::DeviceRef device = oidn::newDevice();
        const char* errorMessage;
        if (device.getError(errorMessage) != oidn::Error::None)
            throw std::runtime_error(errorMessage);
        device.setErrorFunction(errorCallback);
        // Commit the changes to the device
        device.commit();

        // Create the AI filter
        oidn::FilterRef filter = device.newFilter("RT");

        // Set our the filter images
        filter.setImage("color", (void*)&colour_pixels_float3[0], oidn::Format::Float3, c_width, c_height);
        if (a_loaded)
            filter.setImage("albedo", (void*)&albedo_pixels[0], oidn::Format::Float3, a_width, a_height);
        if (n_loaded)
            filter.setImage("normal", (void*)&normal_pixels[0], oidn::Format::Float3, n_width, n_height);
        filter.setImage("output", (void*)&output_pixels[0], oidn::Format::Float3, c_width, c_height);

        // Commit changes to the filter
        filter.commit();

        // Execute denoise
        filter.execute();
    }
    catch (const std::exception& e)
    {
        std::cerr << "[OIDN]: %s", e.what();
        cleanup();
        return -1;
    }


    // If the image already exists delete it
    remove(out_path.c_str());

    // Convert the image back to the original format
    in = (float*)output_pixels.data();
    out = (float*)colour_pixels.data();
    // Convert buffer to float3
    for (unsigned int i = 0; i < output_pixels.size(); i += 3)
    {
        if (!convertToFormat(in, out, 3, colour_roi.nchannels()))
        {
            std::cerr << "Failed to convert output to original format";
            cleanup();
            return -1;
        }
        in += 3;
        out += colour_roi.nchannels();
    }

    // Set our OIIO pixels
    if (!input_colour->set_pixels(colour_roi, OIIO::TypeDesc::FLOAT, &colour_pixels[0]))
        std::cerr <<  "Something went wrong setting pixels";

    // Save the output image
    if (input_colour->write(out_path))
        std::cout << "Done!";
    else
    {
        std::cerr << "Could not save file %s", out_path.c_str();
        std::cerr << "[OIIO]: %s", input_colour->geterror().c_str();
    }

    cleanup();
    return 0;
}
