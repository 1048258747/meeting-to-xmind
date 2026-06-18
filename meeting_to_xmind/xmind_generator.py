import zipfile
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List
from xml.etree.ElementTree import Element, SubElement, tostring, indent
import xml.etree.ElementTree as ET

class XMindGenerator:
    def __init__(self):
        self._topic_counter = 0
    
    def _next_topic_id(self) -> str:
        self._topic_counter += 1
        return f"topic-{self._topic_counter}"
    
    def generate(self, data: Dict[str, Any], output_path: Path):
        content_xml = self._build_content_xml(data)
        manifest_xml = self._build_manifest_xml()
        meta_xml = self._build_meta_xml()
        
        with zipfile.ZipFile(output_path, "w", zipfile.ZIP_DEFLATED) as zf:
            zf.writestr("content.xml", content_xml)
            zf.writestr("META-INF/manifest.xml", manifest_xml)
            zf.writestr("meta.xml", meta_xml)
    
    def generate_multiple(self, files_data: List[Dict[str, Any]], output_dir: Path):
        output_dir.mkdir(parents=True, exist_ok=True)
        
        for i, data in enumerate(files_data, 1):
            filename = f"{i:02d}_{self._sanitize_filename(data['title'])}.xmind"
            output_path = output_dir / filename
            self.generate(data, output_path)
    
    def _build_content_xml(self, data: Dict[str, Any]) -> str:
        xmap = Element("xmap-content")
        xmap.set("xmlns", "urn:xmind:xmap:xmlns:content:2.0")
        xmap.set("xmlns:fo", "http://www.w3.org/1999/XSL/Format")
        xmap.set("xmlns:svg", "http://www.w3.org/2000/svg")
        xmap.set("xmlns:xhtml", "http://www.w3.org/1999/xhtml")
        xmap.set("xmlns:xlink", "http://www.w3.org/1999/xlink")
        
        sheet = SubElement(xmap, "sheet")
        sheet.set("id", "1")
        sheet.set("timestamp", str(int(datetime.now().timestamp() * 1000)))
        
        root_topic = SubElement(sheet, "topic")
        root_topic.set("id", "root")
        root_topic.set("structureClass", "org.xmind.ui.map.unbalanced")
        
        root_title = SubElement(root_topic, "title")
        root_title.text = data.get("title", "Untitled Meeting")
        
        if data.get("date"):
            root_markers = SubElement(root_topic, "markers")
            marker = SubElement(root_markers, "marker")
            marker.set("markerId", "priority-1")
        
        children = SubElement(root_topic, "children")
        topics = SubElement(children, "topics")
        topics.set("type", "attached")
        
        for topic_data in data.get("topics", []):
            self._add_topic(topics, topic_data)
        
        if data.get("action_items"):
            action_topic = SubElement(topics, "topic")
            action_topic.set("id", self._next_topic_id())
            action_title = SubElement(action_topic, "title")
            action_title.text = "Action Items"
            
            action_children = SubElement(action_topic, "children")
            action_topics = SubElement(action_children, "topics")
            action_topics.set("type", "attached")
            
            for item in data["action_items"]:
                item_topic = SubElement(action_topics, "topic")
                item_topic.set("id", self._next_topic_id())
                item_title = SubElement(item_topic, "title")
                
                task_text = item.get("task", "")
                assignee = item.get("assignee", "")
                deadline = item.get("deadline", "")
                
                if assignee:
                    task_text = f"@{assignee}: {task_text}"
                if deadline:
                    task_text = f"{task_text} [{deadline}]"
                
                item_title.text = task_text
        
        indent(xmap)
        return '<?xml version="1.0" encoding="UTF-8"?>\n' + tostring(xmap, encoding="unicode")
    
    def _add_topic(self, parent: Element, topic_data: Dict[str, Any]):
        topic = SubElement(parent, "topic")
        topic.set("id", self._next_topic_id())
        
        title = SubElement(topic, "title")
        title.text = topic_data.get("name", "Untitled")
        
        if topic_data.get("content"):
            notes = SubElement(topic, "notes")
            plain = SubElement(notes, "plain")
            plain.text = topic_data["content"]
        
        subtopics = topic_data.get("subtopics", [])
        if subtopics:
            children = SubElement(topic, "children")
            child_topics = SubElement(children, "topics")
            child_topics.set("type", "attached")
            
            for subtopic in subtopics:
                self._add_topic(child_topics, subtopic)
    
    def _build_manifest_xml(self) -> str:
        manifest = Element("manifest")
        manifest.set("xmlns", "urn:xmind:xmap:xmlns:manifest:1.0")
        
        file_entry = SubElement(manifest, "file-entry")
        file_entry.set("full-path", "/")
        file_entry.set("media-type", "text/xml")
        
        content_entry = SubElement(manifest, "file-entry")
        content_entry.set("full-path", "content.xml")
        content_entry.set("media-type", "text/xml")
        
        indent(manifest)
        return '<?xml version="1.0" encoding="UTF-8"?>\n' + tostring(manifest, encoding="unicode")
    
    def _build_meta_xml(self) -> str:
        meta = Element("meta")
        meta.set("xmlns", "urn:xmind:xmap:xmlns:meta:2.0")
        
        Version = SubElement(meta, "Version")
        Version.text = "2.0"
        
        indent(meta)
        return '<?xml version="1.0" encoding="UTF-8"?>\n' + tostring(meta, encoding="unicode")
    
    def _sanitize_filename(self, name: str) -> str:
        invalid_chars = '<>:"/\\|?*'
        for char in invalid_chars:
            name = name.replace(char, "_")
        return name[:50]
