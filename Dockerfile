FROM python:3.6

ARG project_dir=/app/
ARG dist_dir=/app/dist/

ADD requirements.txt $project_dir
ADD app.py $project_dir
ADD classify_image_graph_def.pb $project_dir
ADD data.json $project_dir
ADD features.npy $project_dir
ADD helper.py $project_dir
ADD dist $dist_dir

WORKDIR $project_dir

RUN pip install -r requirements.txt

CMD ["python", "app.py"]
