import model
import json

class ProjectSerializator:
    def __init__(self, plugins_manager):
        self.plugins_manager = plugins_manager
    
    def parse_file(self, filename):
        myfile = open(filename, 'r')
        json_str = myfile.read()
        return self.parse_json(json_str)
    
    def dump_file(self, project, filename):
        json_str = self.code_json(project)
        myfile = open(filename, 'w+')
        myfile.write(json_str)
    
    def code_json(self, project):
        #if not isinstance(project, model.AnnotationProject):
        #    raise TypeError('The argument project must be an instance of AnnotationProject.')
        
  
        json_project = {}
        json_object = {'AnnotationProject' : json_project}
        json_project['id'] = project.id
        json_project['name'] = project.name
        #if project.main_media:
        json_project['main_media'] = project.main_media
            
        #if project.description:
        json_project['description'] = project.description
        
        #if project.last_modification:
        if project.last_modification == None:
            json_project['last_modification'] = project.last_modification
        else:
            json_project['last_modification'] = project.last_modification.isoformat()
            
        #if project.username:
        json_project['username'] = project.username
            
        json_annotations = []
        json_project['annotations'] = json_annotations
        
        for annotation in project.annotations:
            json_note = annotation.code_json()
            json_annotations.append(json_note)
            

        return json.dumps(json_object, sort_keys=True, indent=4, separators=(',', ': '))
        
    
    def parse_json(self, json_str):
        json_object = json.loads(json_str)
        json_project = json_object['AnnotationProject']
        mid = json_project['id']
        name = json_project['name']
        project = model.AnnotationProject(mid, name)
        project.main_media = json_project['main_media']
        project.description = json_project['description']
        project.last_modification = json_project['last_modification']
        project.username = json_project['username']
        
        json_annotations = json_project['annotations']
        for json_ann in json_annotations:
            if json_ann == None:
                continue
            mtype = json_ann['Annotation']['type']
            annotation_class = self.plugins_manager.get_annotation_class(mtype)
            annotation = annotation_class.parse_json(json_ann)
            project.add_annotation(annotation)
            
        return project
        
    




def test():
    pass

if __name__ == "__main__":
    test()