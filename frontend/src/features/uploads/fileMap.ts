const fileMap = new Map<string, File>();

export const storeFiles = (files: File[]) => {
  files.forEach((file) => fileMap.set(file.name, file));
};

export const getFile = (name: string) => fileMap.get(name);
export const removeFile = (name: string) => fileMap.delete(name);
