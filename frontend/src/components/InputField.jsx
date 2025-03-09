import React from "react";
import { AlertCircle } from "lucide-react";

const InputField = ({ label, type, register, name, errors }) => {
    return (
        <div className="space-y-2">
            <label htmlFor={name} className="block">
                {label} <span className="text-error">*</span>
            </label>
            <input
                id={name}
                type={type}
                {...register(name)}
                className="w-full p-2 border rounded-lg border-border focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent"
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

export default InputField;
