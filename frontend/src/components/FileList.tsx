import {
  Alert,
  CircularProgress,
  Heading,
  Text,
  VStack,
} from "@chakra-ui/react";
import { FC } from "react";
import FileItem from "./FileItem";
import FileForm from "./FileForm";
import { useQuery, useMutation } from "@tanstack/react-query";
import filesApi from "../api/filesApi";
import queryClient from "../api/queryClient";

const FileList: FC = () => {
  const filesQuery = useQuery({
    queryKey: ["file-list"],
    queryFn: filesApi.getFiles,
  });

  const deleteFileMutation = useMutation({
    mutationFn: filesApi.deleteFile,
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ["file-list"] }),
  });

  return (
    <VStack
      w="md"
      maxH="100vh"
      borderRight="1px solid"
      borderColor="gray.200"
      align="stretch"
      gap={4}
      p={4}
    >
      <Heading size="lg" as="h2">
        Файлы
      </Heading>
      <FileForm />
      {filesQuery.isLoading && (
        <CircularProgress isIndeterminate color="teal" />
      )}
      {filesQuery.isError && (
        <Alert status="error">{filesQuery.error.message}</Alert>
      )}
      {filesQuery.data &&
        (filesQuery.data.length === 0 ? (
          <Text size="sm">Нет файлов</Text>
        ) : (
          <VStack overflowY="scroll">
            {filesQuery.data.map((fileTitle) => (
              <FileItem
                key={fileTitle}
                fileTitle={fileTitle}
                onDelete={deleteFileMutation.mutate}
              />
            ))}
          </VStack>
        ))}
    </VStack>
  );
};

export default FileList;
