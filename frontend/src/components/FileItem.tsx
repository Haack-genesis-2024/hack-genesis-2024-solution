import { FC } from "react";
import { FileRecord } from "../types";
import { HStack, Text, Button } from "@chakra-ui/react";

export type FileItemProps = {
  fileRecord: FileRecord;
  onDelete: (fileRecord: FileRecord) => void;
};

const FileItem: FC<FileItemProps> = ({ fileRecord, onDelete }) => {
  return (
    <HStack align="center" justify="space-between" p={2}>
      <Text>{fileRecord.title}</Text>
      <Button variant="outline" onClick={() => onDelete(fileRecord)}>
        Удалить
      </Button>
    </HStack>
  );
};

export default FileItem;
