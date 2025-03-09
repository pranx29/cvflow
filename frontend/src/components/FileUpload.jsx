import React from "react";
import { Controller } from "react-hook-form";
import { Upload, CheckCircle2, AlertCircle } from "lucide-react";

const FileUpload = ({ control, name, label, errors }) => {
    const handleUploadAreaClick = () => {
        document.getElementById(name).click();
    };

    return (
        <div className="space-y-2">
            <label htmlFor={name} className="block">
                {label} <span className="text-error">*</span>
            </label>
            <Controller
                control={control}
                name={name}
                defaultValue={null}
                render={({ field }) => (
                    <div
                        className="mt-1 flex justify-center px-6 py-3 border-2 border-dashed rounded-md border-border hover:border-text-secondary transition-colors cursor-pointer"
                        onClick={handleUploadAreaClick}
                        onDragOver={(e) => {
                            e.preventDefault();
                            e.currentTarget.classList.add(
                                "border-text-secondary"
                            );
                        }}
                        onDragLeave={(e) => {
                            e.currentTarget.classList.remove(
                                "border-text-secondary"
                            );
                        }}
                        onDrop={(e) => {
                            e.preventDefault();
                            e.currentTarget.classList.remove(
                                "border-text-secondary"
                            );
                            field.onChange(e.dataTransfer.files);
                        }}
                    >
                        <div className="space-y-1 text-center text-text-secondary">
                            <Upload className="mx-auto h-12 w-12 " />
                            <div className="flex text-sm">
                                <label
                                    htmlFor={name}
                                    className="relative cursor-pointer rounded-md font-medium text-primary hover:text-primary/80 focus-within:outline-none"
                                >
                                    <input
                                        id={name}
                                        type="file"
                                        accept=".pdf,.docx"
                                        onChange={(e) =>
                                            field.onChange(e.target.files)
                                        }
                                        className="sr-only"
                                    />
                                </label>
                                <p> Upload a file or drag and drop</p>
                            </div>
                            <p className="text-xs text-text-secondary/80">
                                PDF or DOCX up to 10MB
                            </p>
                            {field.value &&
                                field.value[0] && ( // Check if a file is selected
                                    <p className="text-sm text-success-text flex items-center justify-center mt-2">
                                        <CheckCircle2 className="h-4 w-4 mr-1" />
                                        {field.value[0].name}
                                    </p>
                                )}
                        </div>
                    </div>
                )}
            />
            {errors[name] && (
                <p className="text-sm text-error flex items-center mt-1">
                    <AlertCircle className="h-4 w-4 mr-1" />
                    {errors[name]?.message}
                </p>
            )}
        </div>
    );
};

export default FileUpload;
