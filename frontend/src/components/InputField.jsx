import React from "react";
import { AlertCircle } from "lucide-react";

const InputField = ({ label, type, register, name, errors }) => {
    return (
        <div className="space-y-2">
            <label htmlFor={name} className="block font-semibold">
                {label} <span className="text-red-500">*</span>
            </label>
            <input
                id={name}
                type={type}
                {...register(name)}
                className={`w-full p-2 border rounded ${
                    errors[name] ? "border-red-500" : "border-gray-300"
                }`}
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

export default InputField;
