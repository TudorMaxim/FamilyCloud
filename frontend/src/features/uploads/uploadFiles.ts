import familyCloudAPI from '../../api';
import { type AppDispatch } from '../../store';
import { getFile } from './fileMap';
import { type FileUploadTask, updateProgress, setTaskId } from './slice';

const CHUNK_SIZE = 5 * 1024 * 1024; // 5MB
const PARALLEL_BATCHES = 3;

const uploadFiles = async (tasks: FileUploadTask[], dispatch: AppDispatch) => {
  for (let i = 0; i < tasks.length; i += PARALLEL_BATCHES) {
    const batch = tasks.slice(i, i + PARALLEL_BATCHES);

    await Promise.all(
      batch.map(async (task) => {
        const taskId = `${task.name}_${Date.now()}`;
        dispatch(setTaskId({ fileName: task.name, taskId }));

        const eventSource = new EventSource(
          `${import.meta.env.VITE_BACKEND_URL}/progress/${taskId}`
        );
        eventSource.onmessage = (event: MessageEvent) => {
          const data = JSON.parse(event.data);
          dispatch(updateProgress({ taskId, uploadedChunks: data.current }));
          if (data.current === data.total) eventSource.close();
        };

        const totalChunks = Math.ceil(task.size / CHUNK_SIZE);
        for (let chunkIndex = 0; chunkIndex < totalChunks; chunkIndex++) {
          const start = chunkIndex * CHUNK_SIZE;
          const end = Math.min(task.size, start + CHUNK_SIZE);
          const file = getFile(task.name);
          const chunk = file?.slice(start, end);

          const formData = new FormData();
          formData.append('file', chunk ?? '');
          formData.append('chunk_index', chunkIndex.toString());
          formData.append('total_chunks', totalChunks.toString());
          formData.append('task_id', taskId);

          await familyCloudAPI.upload(formData);
        }
      })
    );
  }
};

export default uploadFiles;
