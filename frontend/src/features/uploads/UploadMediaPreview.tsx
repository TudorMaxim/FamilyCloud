import React from 'react';
import { useSelector, useDispatch } from 'react-redux';
import type { RootState, AppDispatch } from '../../store';
import uploadFiles from './uploadFiles';

const UploadMediaPreview = () => {
  const { tasks, overallProgress } = useSelector((state: RootState) => state.uploads);
  const dispatch = useDispatch<AppDispatch>();

  const handleUpload = React.useCallback(async () => {
    await uploadFiles(tasks, dispatch);
  }, [tasks, dispatch]);

  return (
    <div className="container py-3">
      <button className="btn btn-primary mb-3" onClick={handleUpload}>
        Upload All
      </button>

      <div className="progress mb-3" style={{ height: '20px' }}>
        <div
          className="progress-bar progress-bar-striped progress-bar-animated"
          role="progressbar"
          style={{ width: `${overallProgress}%` }}
        >
          {overallProgress}%
        </div>
      </div>

      <div className="row">
        {tasks.map((t, idx) => (
          <div key={idx} className="col-3 mb-3">
            {t.preview ? <img src={t.preview} className="img-fluid mb-1" /> : <span>{t.name}</span>}
            <div className="progress">
              <div
                className="progress-bar progress-bar-striped progress-bar-animated"
                role="progressbar"
                style={{ width: `${t.progress}%` }}
              >
                {t.progress}%
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default UploadMediaPreview;
