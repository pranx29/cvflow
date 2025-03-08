import React from "react";
import { Controller } from "react-hook-form";
import { Upload, CheckCircle2, AlertCircle } from "lucide-react";

const FileUpload = ({ control, name, label, errors }) => {
    const handleUploadAreaClick = () => {
        document.getElementById(name).click();
    };

    return (
        <div className="space-y-2">
            <label htmlFor={name} className="block font-semibold">
                {label} <span className="text-red-500">*</span>
            </label>
            <Controller
                control={control}
                name={name}
                defaultValue={null} 
                render={({ field }) => (
                    <div
                        className="mt-1 flex justify-center px-6 pt-5 pb-6 border-2 border-dashed rounded-md border-gray-300 hover:border-gray-400 transition-colors cursor-pointer"
                        onClick={handleUploadAreaClick}
                    >
                        <div className="space-y-1 text-center">
                            <Upload className="mx-auto h-12 w-12 text-gray-400" />
                            <div className="flex text-sm text-gray-600">
                                <label
                                    htmlFor={name}
                                    className="relative cursor-pointer rounded-md font-medium text-primary hover:text-primary/80 focus-within:outline-none"
                                >
                                    <span>Upload a file</span>
                                    <input
                                        id={name}
                                        type="file"
                                        accept=".pdf,.docx"
                                        onChange={(e) =>
                                            field.onChange(e.target.files)
                                        } // Update field value with selected files
                                        className="sr-only"
                                    />
                                </label>
                                <p className="pl-1">or drag and drop</p>
                            </div>
                            <p className="text-xs text-gray-500">
                                PDF or DOCX up to 10MB
                            </p>
                            {field.value &&
                                field.value[0] && ( // Check if a file is selected
                                    <p className="text-sm text-green-600 flex items-center justify-center mt-2">
                                        <CheckCircle2 className="h-4 w-4 mr-1" />
                                        {field.value[0].name}
                                    </p>
                                )}
                        </div>
                    </div>
                )}
            />
            {errors[name] && (
                <p className="text-sm text-red-500 flex items-center mt-1">
                    <AlertCircle className="h-4 w-4 mr-1" />
                    {errors[name]?.message}
                </p>
            )}
        </div>
    );
};

export default FileUpload;
