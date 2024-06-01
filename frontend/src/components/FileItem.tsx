import { FC } from "react";
import { HStack, Text, Button } from "@chakra-ui/react";

export type FileItemProps = {
  fileTitle: string;
  onDelete: (fileTitle: string) => void;
};

const FileItem: FC<FileItemProps> = ({ fileTitle, onDelete }) => {
  return (
    <HStack align="center" justify="space-between" py={2} w="100%">
      <Text isTruncated>{fileTitle}</Text>
      <Button
        flexShrink={0}
        variant="outline"
        onClick={() => onDelete(fileTitle)}
      >
        Удалить
      </Button>
    </HStack>
  );
};

export default FileItem;
