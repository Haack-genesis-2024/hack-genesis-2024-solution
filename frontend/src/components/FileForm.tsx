import { Button, HStack, Input } from "@chakra-ui/react";
import { FC, FormEvent, useRef } from "react";
import { useMutation } from "@tanstack/react-query";
import filesApi from "../api/filesApi";
import queryClient from "../api/queryClient";

const FileForm: FC = () => {
  const inputFileRef = useRef<HTMLInputElement>(null);

  const { mutate, isPending } = useMutation({
    mutationFn: filesApi.uploadFile,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["file-list"] });
      inputFileRef.current!.value = "";
    },
  });

  const onUploadFile = (e: FormEvent) => {
    e.preventDefault();

    const file = inputFileRef.current?.files?.[0];

    if (file) {
      const formData = new FormData();
      formData.append("file", file);
      mutate(formData);
    }
  };

  return (
    <HStack as="form" gap={2} onSubmit={onUploadFile}>
      <Input type="file" required ref={inputFileRef} />
      <Button
        isLoading={isPending}
        type="submit"
        flexShrink={0}
        colorScheme="teal"
      >
        Загрузить
      </Button>
    </HStack>
  );
};

export default FileForm;
