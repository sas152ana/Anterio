import sys
import ctypes
import sdl2
import sdl2.ext
import pygame 
from pygame.locals import * 
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np 
import math
import uuid
import json
import copy
import colorsys
import os
import time
import datetime
import string
import zipfile
import io
import tempfile
import shutil
import trimesh
import trimesh.creation
import trimesh.visual
import traceback
import threading
import subprocess
from PIL import Image
import string
from shapely.geometry import box as shapely_box
from shapely.ops import unary_union
import imageio
import locale
WINDOW_SIZE = (1600, 900)
FOV = 60
NEAR_CLIP = 0.2
FAR_CLIP = 1000.0
COLOR_SKY = (0.529, 0.808, 0.922)
COLOR_NIGHT = (0.05, 0.05, 0.1)
COLOR_GROUND = (0.2, 0.5, 0.2)
COLOR_SELECTION = (1.0, 1.0, 0.0)
COLOR_PREVIEW = (0.0, 1.0, 1.0)
COLOR_VELOCITY_MIN = (0.0, 0.0, 0.5) # Темно-синий
COLOR_VELOCITY_MAX = (1.0, 0.7, 0.8) # Светло-розовый
SHADE_TOP_BOTTOM = 1.00
SHADE_NS = 0.90
SHADE_EW = 0.84
UV_SCALE = 0.05
FLOOR_SIZE = 400
MAX_MIRRORS = 20
if sys.platform == "win32":
    try:
        ctypes.windll.shcore.SetProcessDpiAwareness(2)
    except Exception:
        try:
            ctypes.windll.user32.SetProcessDPIAware()
        except:
            pass
# Коды стран, где распространен русский язык
RU_LOCALES = ['ru', 'be', 'uk', 'kk', 'ky', 'uz', 'tg', 'ab', 'os']

TRANSLATIONS = {
    'en': {
        # Main Menu & UI
        'GAMENAME': 'ANTERIO',
        'RESUME_PROJECT': 'RESUME PROJECT',
        'NEW_PROJECT': 'NEW PROJECT',
        'LOAD_PROJECT': 'LOAD PROJECT',
        'QUIT': 'QUIT',
        'RESUME': 'RESUME',
        'SAVE_PROJECT': 'SAVE PROJECT',
        'EXPORT_3D': 'EXPORT 3D...',
        'CLEAR_SCENE': 'CLEAR SCENE',
        'MAIN_MENU': 'MAIN MENU',
        'FPS_LIMIT_ON': 'FPS LIMIT: ON',
        'FPS_LIMIT_OFF': 'FPS LIMIT: OFF',
        'FOG_DIST': 'Fog Distance',
        'WALL_THICK': 'New Wall Thickness',
        'SAVE_EXIT': 'SAVE & EXIT',
        'DONT_SAVE': "DON'T SAVE",
        'CANCEL': 'CANCEL',
        'SAVE_QUESTION': 'Save changes?',
        'PAUSED': 'PAUSED',
        'LANGUAGE': 'LANGUAGE: ENGLISH',
        'FD_VIEW_BTN': 'View',
        'ERR_TEX_LOAD': 'FAILED TO LOAD TEXTURE',
        'NOTIF_DOOR_GRP_REMOVED': 'DOOR GROUP REMOVED',
        'NOTIF_EMERGENCY_RESPAWN': 'EMERGENCY RESPAWN',
        'ERR_MULTIPLE_CAMS': 'CANNOT EDIT POS OF MULTIPLE CAMERAS',
        'ERR_NEED_2_KEYS': 'Need at least 2 keyframes!',
        'NOTIF_UNDO_CAM': 'UNDO (CAMERA)',
        'NOTIF_REDO_CAM': 'REDO (CAMERA)',
        'NOTIF_EDIT_CANCELED': 'EDIT CANCELED', # Был в словаре, но проверим
        # Tools & HUD
        'TOOL': 'Tool',
        'AXIS': 'Axis',
        'VERT': 'Vert',
        'SNAP': 'Snap',
        'SIZE': 'Size',
        'CONSTR': 'Constr',
        'MODE': 'Mode',
        'VERTICAL': 'Vertical',
        'HORIZONTAL': 'Horizontal',
        'SELECT': 'SELECT',
        'WALL': 'WALL',
        'BOX': 'BOX',
        'ROOM': 'ROOM',
        'STRIP': 'STRIP',
        'CUBE': 'CUBE',
        'CUT': 'CUT',
        'SLICE': 'SLICE',
        'DOOR_CREATOR': 'DOOR CREATOR',
        'SUN_EDITOR': 'SUN EDITOR',
        'HINT_GAME': '[Q] Vert/Flat | [Ctrl+Q] Cycle Axis | [E] Resize | [R] Rotate | [F] Flip | [G] Group | [T] Door',
        'HINT_SUN': '[Up/Down] Time | [Ctrl+Up/Down] Speed (Std: 2.5) | [Enter] Apply',
        'HINT_CUBE': 'Size: 1dm (Def) | 0.5m (Shift) | 1cm (Ctrl)',
        'SUN_INFO': 'Time: {time}° | Rot: {rot}° | Speed: {speed:.1f}',
        'MOVE': 'MOVE',
        'RESIZE': 'RESIZE',
        
        # Color Picker
        'CP_HUE': 'Hue', 'CP_SAT': 'Sat', 'CP_VAL': 'Val',
        'CP_ALPHA': 'Alpha', 'CP_EMIT': 'Emit', 'CP_GLOSS': 'Gloss',
        'CP_DENS': 'Dens', 'CP_MIRR': 'Mirr',
        'CP_FULL': 'Full', 'CP_TILE': 'Tile',
        'CP_LOAD_TEX': 'Load Texture',
        'CP_NO_TEX': 'No Texture',
        'CP_FILE': 'File', 'CP_DATA': 'Data',
        
        # File Dialog
        'FD_DESKTOP': 'Desktop', 'FD_DOCS': 'Documents', 'FD_DOWN': 'Downloads',
        'FD_VIEW': 'View', 'FD_NAME': 'Name', 'FD_DATE': 'Date', 'FD_SIZE': 'Size',
        'FD_OK': 'OK', 'FD_CANCEL': 'Cancel', 'FD_FMT': 'FMT',
        
        # Camera Manager
        'CAM_MODE': 'CINE CAM MODE',
        'CAM_SLOT': 'Slot',
        'CAM_EDITING': '[EDITING]',
        'CAM_SMOOTH': '[SMOOTHING MODE]',
        'CAM_TOTAL': 'Total Time',
        'CAM_KEYS': 'Keyframes',
        'CAM_LOOP': 'Loop',
        'CAM_HINT_1': '[Enter] Add/Edit | [Del] Delete | [Esc] Exit',
        'CAM_HINT_2': '[Arrows] Duration | [Ctrl+Arrows] Smoothing',
        'CAM_HINT_3': '[RMB] Rect Select',
        'CAM_SEL_ONE': 'SELECTED: Keyframe',
        'CAM_SEL_MANY': 'SELECTED: {count} Keyframes',
        'CAM_DUR': 'Duration',
        'CAM_LOOP_T': 'Loop Time',
        'CAM_SMOOTHNESS': 'Smoothness',
        'CAM_EASE': 'Ease',
        'CAM_AT': 'At',
        'CAM_REORDER': '[Shift+Arrows] Reorder',
        'CAM_ON': 'ON',
        'CAM_OFF': 'OFF',
        'CAM_SEC': 's',
        'CAM_OTHERS': ' (+others)',
        
        # Notifications
        'NOTIF_UNDO': 'UNDO',
        'NOTIF_REDO': 'REDO',
        'NOTIF_SAVED': 'PROJECT SAVED!',
        'NOTIF_EXPORT': 'EXPORTING... PLEASE WAIT',
        'NOTIF_EXPORT_OK': 'SAVED: {name}',
        'NOTIF_GROUP_DISSOLVED': 'GROUP DISSOLVED',
        'NOTIF_GROUP_CREATED': 'GROUP CREATED',
        'NOTIF_COPIED': 'COPIED TO CLIPBOARD',
        'NOTIF_OBJ_DELETED': 'OBJECTS DELETED',
        'NOTIF_PROPS_COPIED': 'PROPERTIES COPIED',
        'NOTIF_SETTINGS_APPLIED': 'SETTINGS APPLIED',
        'NOTIF_TEX_APPLIED': 'TEXTURE APPLIED',
        'NOTIF_TEX_REMOVED': 'TEXTURE REMOVED',
        'NOTIF_DOOR_CREATED': 'DOOR CREATED',
        'NOTIF_DOOR_REMOVED': 'DOOR REMOVED',
        'NOTIF_DOOR_FLIPPED': 'DOOR STATE FLIPPED',
        'NOTIF_CUBE_CUT': 'CUBE CUT APPLIED',
        'NOTIF_HOLE_CREATED': 'BASEMENT HOLE CREATED',
        'NOTIF_MERGED': 'OBJECTS MERGED',
        'NOTIF_RENDER_DONE': 'RENDER DONE',
        'NOTIF_RENDER_ERR': 'RENDER ERROR',
        'NOTIF_CINE_ON': 'CINE CAMERA MODE: ON',
        'NOTIF_CINE_OFF': 'CINE CAMERA MODE: OFF',
        'NOTIF_CINE_RESTORED': 'CINE CAMERA MODE: RESTORED',
        'NOTIF_POS_UPDATED': 'POSITION UPDATED',
        'NOTIF_KEY_ADDED': 'KEYFRAME ADDED',
        'NOTIF_KEY_DELETED': 'KEYFRAMES DELETED',
        'NOTIF_EDIT_CANCELED': 'EDIT CANCELED',
        'NOTIF_NO_PAINT_HOLES': 'CANNOT PAINT HOLES',
        'NOTIF_CANT_FLIP_HOLES': 'CANNOT FLIP HOLES',
        'NOTIF_HOLES_ROT_H': 'HOLES CAN ONLY ROTATE HORIZONTALLY',
        'NOTIF_SAFE_SPOT': 'RETURNED TO SAFE SPOT',
        'NOTIF_RESPAWN': 'RESPAWNED ON NEAREST GROUND',
    },
    'ru': {
        # Main Menu & UI
        'GAMENAME': 'АНТЕРИО',
        'RESUME_PROJECT': 'ПРОДОЛЖИТЬ',
        'NEW_PROJECT': 'НОВЫЙ ПРОЕКТ',
        'LOAD_PROJECT': 'ЗАГРУЗИТЬ',
        'QUIT': 'ВЫХОД',
        'RESUME': 'ПРОДОЛЖИТЬ',
        'SAVE_PROJECT': 'СОХРАНИТЬ',
        'EXPORT_3D': 'ЭКСПОРТ 3D...',
        'CLEAR_SCENE': 'ОЧИСТИТЬ СЦЕНУ',
        'MAIN_MENU': 'ГЛАВНОЕ МЕНЮ',
        'FPS_LIMIT_ON': 'FPS ЛИМИТ: ВКЛ',
        'FPS_LIMIT_OFF': 'FPS ЛИМИТ: ВЫКЛ',
        'FOG_DIST': 'Дальность тумана',
        'WALL_THICK': 'Толщина новых стен',
        'SAVE_EXIT': 'СОХРАНИТЬ И ВЫЙТИ',
        'DONT_SAVE': "НЕ СОХРАНЯТЬ",
        'CANCEL': 'ОТМЕНА',
        'SAVE_QUESTION': 'Сохранить изменения?',
        'PAUSED': 'ПАУЗА',
        'LANGUAGE': 'ЯЗЫК: РУССКИЙ',
        'FD_VIEW_BTN': 'Вид',
        'ERR_TEX_LOAD': 'ОШИБКА ЗАГРУЗКИ ТЕКСТУРЫ',
        'NOTIF_DOOR_GRP_REMOVED': 'ГРУППА ДВЕРЕЙ УДАЛЕНА',
        'NOTIF_EMERGENCY_RESPAWN': 'АВАРИЙНОЕ ВОЗРОЖДЕНИЕ',
        'ERR_MULTIPLE_CAMS': 'НЕЛЬЗЯ МЕНЯТЬ ПОЗ. НЕСКОЛЬКИХ КАМЕР',
        'ERR_NEED_2_KEYS': 'Нужно минимум 2 кадра!',
        'NOTIF_UNDO_CAM': 'ОТМЕНА (КАМЕРА)',
        'NOTIF_REDO_CAM': 'ПОВТОР (КАМЕРА)',
        'NOTIF_EDIT_CANCELED': 'РЕДАКТИРОВАНИЕ ОТМЕНЕНО',
        # Tools & HUD
        'TOOL': 'Инстр.',
        'AXIS': 'Ось',
        'VERT': 'Верт.',
        'SNAP': 'Сетка',
        'SIZE': 'Разм.',
        'CONSTR': 'Огр.',
        'MODE': 'Режим',
        'VERTICAL': 'Вертикально',
        'HORIZONTAL': 'Горизонтально',
        'SELECT': 'ВЫБОР',
        'WALL': 'СТЕНА',
        'BOX': 'КОРОБКА',
        'ROOM': 'КОМНАТА',
        'STRIP': 'ПОЛОСА',
        'CUBE': 'КУБ',
        'CUT': 'ВЫРЕЗ',
        'SLICE': 'РАЗРЕЗ',
        'DOOR_CREATOR': 'ДВЕРИ',
        'SUN_EDITOR': 'РЕДАКТОР СОЛНЦА',
        'HINT_GAME': '[Q] Ось/Плоск | [Ctrl+Q] Цикл Оси | [E] Размер | [R] Вращ. | [F] Зеркало | [G] Группа | [T] Дверь',
        'HINT_SUN': '[Стрелки] Время | [Ctrl+Стрелки] Скорость | [Enter] Принять',
        'HINT_CUBE': 'Разм: 1дм (Станд) | 0.5м (Shift) | 1см (Ctrl)',
        'SUN_INFO': 'Время: {time}° | Поворот: {rot}° | Скор: {speed:.1f}',
        'MOVE': 'ПЕРЕМЕЩЕНИЕ',
        'RESIZE': 'РАЗМЕР',
        
        # Color Picker
        'CP_HUE': 'Тон', 'CP_SAT': 'Нас.', 'CP_VAL': 'Ярк.',
        'CP_ALPHA': 'Прозр.', 'CP_EMIT': 'Свеч.', 'CP_GLOSS': 'Глян.',
        'CP_DENS': 'Плотн.', 'CP_MIRR': 'Зерк.',
        'CP_FULL': 'Все', 'CP_TILE': 'Тайл',
        'CP_LOAD_TEX': 'Загрузить Текстуру',
        'CP_NO_TEX': 'Нет Текстуры',
        'CP_FILE': 'Файл', 'CP_DATA': 'Данные',
        
        # File Dialog
        'FD_DESKTOP': 'Рабочий стол', 'FD_DOCS': 'Документы', 'FD_DOWN': 'Загрузки',
        'FD_VIEW': 'Вид', 'FD_NAME': 'Имя', 'FD_DATE': 'Дата', 'FD_SIZE': 'Размер',
        'FD_OK': 'ОК', 'FD_CANCEL': 'Отмена', 'FD_FMT': 'ФОРМАТ',
        
        # Camera Manager
        'CAM_MODE': 'РЕЖИМ КИНО-КАМЕРЫ',
        'CAM_SLOT': 'Слот',
        'CAM_EDITING': '[РЕДАКТИРОВАНИЕ]',
        'CAM_SMOOTH': '[СГЛАЖИВАНИЕ]',
        'CAM_TOTAL': 'Всего',
        'CAM_KEYS': 'Кадров',
        'CAM_LOOP': 'Цикл',
        'CAM_HINT_1': '[Enter] Доб/Ред | [Del] Удал | [Esc] Выход',
        'CAM_HINT_2': '[Стрелки] Длительность | [Ctrl+Стрелки] Сглаживание',
        'CAM_HINT_3': '[ПКМ] Выделение рамкой',
        'CAM_SEL_ONE': 'ВЫБРАН: Кадр',
        'CAM_SEL_MANY': 'ВЫБРАНО: {count} Кадров',
        'CAM_DUR': 'Длительность',
        'CAM_LOOP_T': 'Время цикла',
        'CAM_SMOOTHNESS': 'Плавность',
        'CAM_EASE': 'Смягчение',
        'CAM_AT': 'На',
        'CAM_REORDER': '[Shift+Стрелки] Порядок',
        'CAM_ON': 'ВКЛ',
        'CAM_OFF': 'ВЫКЛ',
        'CAM_SEC': 'с',
        'CAM_OTHERS': ' (+др.)',
        
        # Notifications
        'NOTIF_UNDO': 'ОТМЕНА (UNDO)',
        'NOTIF_REDO': 'ПОВТОР (REDO)',
        'NOTIF_SAVED': 'ПРОЕКТ СОХРАНЕН!',
        'NOTIF_EXPORT': 'ЭКСПОРТ... ЖДИТЕ',
        'NOTIF_EXPORT_OK': 'СОХРАНЕНО: {name}',
        'NOTIF_GROUP_DISSOLVED': 'ГРУППА РАСФОРМИРОВАНА',
        'NOTIF_GROUP_CREATED': 'ГРУППА СОЗДАНА',
        'NOTIF_COPIED': 'СКОПИРОВАНО В БУФЕР',
        'NOTIF_OBJ_DELETED': 'ОБЪЕКТЫ УДАЛЕНЫ',
        'NOTIF_PROPS_COPIED': 'СВОЙСТВА СКОПИРОВАНЫ',
        'NOTIF_SETTINGS_APPLIED': 'НАСТРОЙКИ ПРИМЕНЕНЫ',
        'NOTIF_TEX_APPLIED': 'ТЕКСТУРА ПРИМЕНЕНА',
        'NOTIF_TEX_REMOVED': 'ТЕКСТУРА УДАЛЕНА',
        'NOTIF_DOOR_CREATED': 'ДВЕРЬ СОЗДАНА',
        'NOTIF_DOOR_REMOVED': 'ДВЕРЬ УДАЛЕНА',
        'NOTIF_DOOR_FLIPPED': 'ДВЕРЬ ПЕРЕВЕРНУТА',
        'NOTIF_CUBE_CUT': 'ВЫРЕЗ ПРИМЕНЕН',
        'NOTIF_HOLE_CREATED': 'ОТВЕРСТИЕ В ПОЛУ СОЗДАНО',
        'NOTIF_MERGED': 'ОБЪЕКТЫ ОБЪЕДИНЕНЫ',
        'NOTIF_RENDER_DONE': 'РЕНДЕР ЗАВЕРШЕН',
        'NOTIF_RENDER_ERR': 'ОШИБКА РЕНДЕРА',
        'NOTIF_CINE_ON': 'РЕЖИМ КИНО-КАМЕРЫ: ВКЛ',
        'NOTIF_CINE_OFF': 'РЕЖИМ КИНО-КАМЕРЫ: ВЫКЛ',
        'NOTIF_CINE_RESTORED': 'КИНО-КАМЕРА: ВОССТАНОВЛЕНО',
        'NOTIF_POS_UPDATED': 'ПОЗИЦИЯ ОБНОВЛЕНА',
        'NOTIF_KEY_ADDED': 'КАДР ДОБАВЛЕН',
        'NOTIF_KEY_DELETED': 'КАДРЫ УДАЛЕНЫ',
        'NOTIF_EDIT_CANCELED': 'РЕДАКТИРОВАНИЕ ОТМЕНЕНО',
        'NOTIF_NO_PAINT_HOLES': 'НЕЛЬЗЯ КРАСИТЬ ДЫРЫ',
        'NOTIF_CANT_FLIP_HOLES': 'НЕЛЬЗЯ ОТРАЖАТЬ ДЫРЫ',
        'NOTIF_HOLES_ROT_H': 'ДЫРЫ ВРАЩАЮТСЯ ТОЛЬКО ГОРИЗОНТАЛЬНО',
        'NOTIF_SAFE_SPOT': 'ВОЗВРАТ В БЕЗОПАСНОЕ МЕСТО',
        'NOTIF_RESPAWN': 'ВОЗРОЖДЕНИЕ НА ЗЕМЛЕ',
    }
}
class AnimatedTexture:
    def __init__(self, tex_id, width, height, frames_data):
        self.tex_id = tex_id
        self.width = width
        self.height = height
        self.frames = frames_data
        self.frame_count = len(frames_data)
        self.current_frame = 0
        self.timer = 0.0
        if self.frame_count > 0:
            self._upload_frame(0)
    def update(self, dt):
        if self.frame_count <= 1: return
        self.timer += dt * 1000.0
        current_delay = self.frames[self.current_frame][1]
        if current_delay <= 0: current_delay = 100 
        if self.timer >= current_delay:
            self.timer -= current_delay
            self.current_frame = (self.current_frame + 1) % self.frame_count
            self._upload_frame(self.current_frame)
    def _upload_frame(self, frame_idx):
        data = self.frames[frame_idx][0]
        glBindTexture(GL_TEXTURE_2D, self.tex_id)
        glTexSubImage2D(GL_TEXTURE_2D, 0, 0, 0, self.width, self.height, GL_RGBA, GL_UNSIGNED_BYTE, data)
        glGenerateMipmap(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, 0)
class MatrixUtils:
    @staticmethod
    def identity():
        return np.identity(4, dtype=np.float32)
    @staticmethod
    def translation(x, y, z):
        m = np.identity(4, dtype=np.float32)
        m[0, 3] = x
        m[1, 3] = y
        m[2, 3] = z
        return m
    @staticmethod
    def scale(x, y, z):
        m = np.identity(4, dtype=np.float32)
        m[0, 0] = x
        m[1, 1] = y
        m[2, 2] = z
        return m
    @staticmethod
    def rotation_y(angle_deg):
        rad = math.radians(angle_deg)
        c, s = math.cos(rad), math.sin(rad)
        m = np.identity(4, dtype=np.float32)
        m[0, 0] = c
        m[0, 2] = s  
        m[2, 0] = -s
        m[2, 2] = c
        return m
    @staticmethod
    def rotation_x(angle_deg):
        rad = math.radians(angle_deg)
        c, s = math.cos(rad), math.sin(rad)
        m = np.identity(4, dtype=np.float32)
        m[1, 1] = c
        m[1, 2] = -s
        m[2, 1] = s
        m[2, 2] = c
        return m
    @staticmethod
    def ortho_2d(left, right, bottom, top):
        m = np.identity(4, dtype=np.float32)
        m[0, 0] = 2.0 / (right - left)
        m[1, 1] = 2.0 / (top - bottom)
        m[2, 2] = -1.0
        m[0, 3] = -(right + left) / (right - left)
        m[1, 3] = -(top + bottom) / (top - bottom)
        return m
    @staticmethod
    def rotation_z(angle_deg):
        rad = math.radians(angle_deg)
        c, s = math.cos(rad), math.sin(rad)
        m = np.identity(4, dtype=np.float32)
        m[0, 0] = c
        m[0, 1] = -s
        m[1, 0] = s
        m[1, 1] = c
        return m
    @staticmethod
    def perspective(fov, aspect, near, far):
        f = 1.0 / math.tan(math.radians(fov) / 2.0)
        m = np.zeros((4, 4), dtype=np.float32)
        m[0, 0] = f / aspect
        m[1, 1] = f
        m[2, 2] = (far + near) / (near - far)
        m[2, 3] = (2.0 * far * near) / (near - far)
        m[3, 2] = -1.0
        return m
    @staticmethod
    def ortho(left, right, bottom, top, near, far):
        m = np.identity(4, dtype=np.float32)
        m[0, 0] = 2.0 / (right - left)
        m[1, 1] = 2.0 / (top - bottom)
        m[2, 2] = -2.0 / (far - near)
        m[0, 3] = -(right + left) / (right - left)
        m[1, 3] = -(top + bottom) / (top - bottom)
        m[2, 3] = -(far + near) / (far - near)
        return m
    @staticmethod
    def look_at(eye, center, up):
        f = center - eye
        f /= np.linalg.norm(f) 
        s = np.cross(f, up) 
        s /= np.linalg.norm(s)
        u = np.cross(s, f) 
        m = np.identity(4, dtype=np.float32)
        m[0, 0] = s[0]; m[0, 1] = s[1]; m[0, 2] = s[2]
        m[1, 0] = u[0]; m[1, 1] = u[1]; m[1, 2] = u[2]
        m[2, 0] = -f[0]; m[2, 1] = -f[1]; m[2, 2] = -f[2]
        m[0, 3] = -np.dot(s, eye)
        m[1, 3] = -np.dot(u, eye)
        m[2, 3] = np.dot(f, eye)
        return m
    @staticmethod
    def multiply_vec4(mat, vec):
        return np.dot(mat, vec)
    @staticmethod
    def unproject(win_x, win_y, win_z, view, proj, viewport):
        x = (win_x - viewport[0]) / viewport[2] * 2.0 - 1.0
        y = (win_y - viewport[1]) / viewport[3] * 2.0 - 1.0
        z = 2.0 * win_z - 1.0
        clip_pos = np.array([x, y, z, 1.0], dtype=np.float32)
        inv_pv = np.linalg.inv(proj @ view)
        world_pos = np.dot(inv_pv, clip_pos)
        if world_pos[3] == 0:
            return None
        return world_pos[:3] / world_pos[3]
    @staticmethod
    def project(obj_x, obj_y, obj_z, view, proj, viewport):
        pos = np.array([obj_x, obj_y, obj_z, 1.0], dtype=np.float32)
        clip = np.dot(proj @ view, pos)
        if clip[3] == 0:
            return None
        ndc = clip[:3] / clip[3]
        win_x = viewport[0] + (ndc[0] + 1.0) / 2.0 * viewport[2]
        win_y = viewport[1] + (ndc[1] + 1.0) / 2.0 * viewport[3]
        win_z = (ndc[2] + 1.0) / 2.0
        return win_x, win_y, win_z
class CubeRenderer:
    def __init__(self, texture_manager):
        dummy_ent = Entity(np.array([0,0,0]), np.array([1,1,1]))
        dummy_ent.faces_colors = [[1,1,1,1]] * 6
        batches = ChunkMeshBuilder.build_chunk_data([dummy_ent], (0, 0, 0), texture_manager)
        all_data = []
        for data_array in batches.values():
            all_data.extend(data_array)
        data_np = np.array(all_data, dtype=np.float32)
        self.mesh = MeshBuffer(data_np)
    def draw(self):
        self.mesh.draw()
    def delete(self):
        self.mesh.delete()
class Framebuffer:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.fbo = glGenFramebuffers(1)
        self.tex = glGenTextures(1)
        self.rbo = glGenRenderbuffers(1)
        self.resize(width, height)
    def resize(self, width, height):
        self.width = width
        self.height = height
        glBindFramebuffer(GL_FRAMEBUFFER, self.fbo)
        glBindTexture(GL_TEXTURE_2D, self.tex)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, width, height, 0, GL_RGB, GL_UNSIGNED_BYTE, None)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
        glFramebufferTexture2D(GL_FRAMEBUFFER, GL_COLOR_ATTACHMENT0, GL_TEXTURE_2D, self.tex, 0)
        glBindRenderbuffer(GL_RENDERBUFFER, self.rbo)
        glRenderbufferStorage(GL_RENDERBUFFER, GL_DEPTH24_STENCIL8, width, height)
        glFramebufferRenderbuffer(GL_FRAMEBUFFER, GL_DEPTH_STENCIL_ATTACHMENT, GL_RENDERBUFFER, self.rbo)
        if glCheckFramebufferStatus(GL_FRAMEBUFFER) != GL_FRAMEBUFFER_COMPLETE:
            print("ERROR: Framebuffer is not complete!")
        glBindFramebuffer(GL_FRAMEBUFFER, 0)
    def bind(self):
        glBindFramebuffer(GL_FRAMEBUFFER, self.fbo)
        glViewport(0, 0, self.width, self.height)
    def unbind(self, scr_width, scr_height):
        glBindFramebuffer(GL_FRAMEBUFFER, 0)
        glViewport(0, 0, scr_width, scr_height)
    def delete(self):
        glDeleteFramebuffers(1, [self.fbo])
        glDeleteTextures([self.tex])
        glDeleteRenderbuffers(1, [self.rbo])
class TextureManager:
    def __init__(self):
        self.textures = {} 
        self.reverse_lookup = {} 
        self.white_tex_id = None 
        self.animated_textures = [] 
    def get_white_texture(self):
        if self.white_tex_id is None:
            surf = pygame.Surface((2, 2))
            surf.fill((255, 255, 255))
            self.white_tex_id = upload_texture_to_gpu(surf)
        return self.white_tex_id
    def update(self, dt):
        for anim in self.animated_textures:
            anim.update(dt)
    def _load_gif_content(self, pil_image, name_key):
        frames = []
        try:
            while True:
                frame = pil_image.convert("RGBA")
                frame = frame.transpose(Image.FLIP_TOP_BOTTOM)
                duration = pil_image.info.get('duration', 100) 
                data = frame.tobytes()
                frames.append((data, duration))
                pil_image.seek(pil_image.tell() + 1)
        except EOFError:
            pass 
        if not frames: return None
        w, h = pil_image.size
        tex_id = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, tex_id)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, w, h, 0, GL_RGBA, GL_UNSIGNED_BYTE, frames[0][0])
        glGenerateMipmap(GL_TEXTURE_2D)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glBindTexture(GL_TEXTURE_2D, 0)
        if len(frames) > 1:
            anim_obj = AnimatedTexture(tex_id, w, h, frames)
            self.animated_textures.append(anim_obj)
        self.textures[name_key] = {
            'id': tex_id,
            'w': w,
            'h': h,
        }
        self.reverse_lookup[tex_id] = name_key
        return tex_id
    def load_from_file(self, filepath):
        if filepath in self.textures: return self.textures[filepath]['id']
        norm_path = os.path.abspath(filepath)
        if norm_path in self.textures: return self.textures[norm_path]['id']
        if Image and filepath.lower().endswith('.gif'):
            try:
                img = Image.open(norm_path)
                tex_id = self._load_gif_content(img, norm_path)
                self.textures[filepath] = self.textures[norm_path] 
                print(f"GIF Loaded: {filepath} -> ID {tex_id}")
                return tex_id
            except Exception as e:
                print(f"GIF load failed, falling back to Pygame: {e}")
        try:
            surf = pygame.image.load(norm_path) 
            tex_id = upload_texture_to_gpu(surf, wrap_mode=GL_REPEAT)
            self.textures[norm_path] = {
                'id': tex_id,
                'w': surf.get_width(),
                'h': surf.get_height(),
            }
            self.reverse_lookup[tex_id] = norm_path
            self.textures[filepath] = self.textures[norm_path]
            print(f"Texture loaded: {filepath} -> ID {tex_id}")
            return tex_id
        except Exception as e:
            return None
    def load_from_memory(self, name, file_obj):
        if name in self.textures: return self.textures[name]['id']
        if Image and name.lower().endswith('.gif'):
            try:
                img = Image.open(file_obj)
                tex_id = self._load_gif_content(img, name)
                return tex_id
            except Exception as e:
                print(f"Memory GIF failed: {e}")
                file_obj.seek(0) 
        try:
            surf = pygame.image.load(file_obj)
            tex_id = upload_texture_to_gpu(surf, wrap_mode=GL_REPEAT)
            self.textures[name] = {'id': tex_id, 'w': surf.get_width(), 'h': surf.get_height()}
            self.reverse_lookup[tex_id] = name
            return tex_id
        except Exception as e:
            print(f"Failed to load texture from memory {name}: {e}")
            return None
    def get_texture_path_by_id(self, tex_id):
        return self.reverse_lookup.get(tex_id, None)
class SpriteRenderer:
    def __init__(self):
        self.vertices = [] 
        self.vbo = glGenBuffers(1)
        self.vao = glGenVertexArrays(1)
        self.max_sprites = 10000 
        self.shader = Shader("""
            #version 330 core
            layout (location = 0) in vec3 aPos;
            layout (location = 1) in vec4 aColor;
            layout (location = 2) in vec2 aTex;
            uniform mat4 view;
            uniform mat4 projection;
            out vec4 vColor;
            out vec2 vTex;
            void main() {
                gl_Position = projection * view * vec4(aPos, 1.0);
                vColor = aColor;
                vTex = aTex;
            }
        """, """
            #version 330 core
            out vec4 FragColor;
            in vec4 vColor;
            in vec2 vTex;
            uniform sampler2D uTex;
            uniform int uMode; 
            void main() {
                vec4 finalColor = vColor;
                if (uMode == 0) {
                    // --- ТЕКСТУРА (UI, Солнце) ---
                    vec4 texColor = texture(uTex, vTex);
                    if(texColor.a < 0.05) discard;
                    finalColor = texColor * vColor;
                } else if (uMode == 1) {
                    // --- ИКОНКА ЛАМПЫ ---
                    vec2 uv = vTex - 0.5;
                    float dist = length(uv);
                    float ring = smoothstep(0.45, 0.40, dist) * smoothstep(0.30, 0.35, dist);
                    float dot = smoothstep(0.15, 0.10, dist);
                    float alpha = max(ring, dot);
                    if (alpha < 0.01) discard;
                    finalColor = vec4(1.0, 1.0, 1.0, alpha) * vColor;
                } else if (uMode == 2) {
                    // --- СЕТКА (GRID) ---
                    // vTex здесь содержит метрические координаты от центра грани (в метрах)
                    float spacing = 0.5; // Шаг сетки
                    // Магия шейдеров: рисуем линии толщиной в 1.5 пикселя экрана
                    // fwidth позволяет узнать, сколько 'метров' в одном пикселе экрана
                    // Вычисляем расстояние до ближайшей линии сетки
                    vec2 grid = abs(fract(vTex / spacing + 0.5) - 0.5) / fwidth(vTex / spacing);
                    // Выбираем минимальное расстояние (линия X или Y)
                    float line = min(grid.x, grid.y);
                    // Рисуем линию: 1.0 если мы на линии, 0.0 если далеко
                    // 1.5 - это толщина линии в пикселях (можно менять)
                    float alpha = 1.0 - min(line, 1.0);
                    // Только линии, остальное прозрачно
                    if (alpha < 0.1) discard;
                    finalColor = vec4(vColor.rgb, vColor.a * alpha);
                }
                FragColor = finalColor;
            }
        """)
        glBindVertexArray(self.vao)
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        glBufferData(GL_ARRAY_BUFFER, self.max_sprites * 6 * 9 * 4, None, GL_DYNAMIC_DRAW)
        stride = 9 * 4
        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, stride, ctypes.c_void_p(0))
        glEnableVertexAttribArray(1)
        glVertexAttribPointer(1, 4, GL_FLOAT, GL_FALSE, stride, ctypes.c_void_p(12))
        glEnableVertexAttribArray(2)
        glVertexAttribPointer(2, 2, GL_FLOAT, GL_FALSE, stride, ctypes.c_void_p(28))
        glBindVertexArray(0)
    def add_quad(self, p1, p2, p3, p4, color=(1,1,1,1)):
        c = list(color)
        self.vertices.extend([*p1, *c, 0, 0]) 
        self.vertices.extend([*p2, *c, 1, 0]) 
        self.vertices.extend([*p3, *c, 1, 1]) 
        self.vertices.extend([*p1, *c, 0, 0]) 
        self.vertices.extend([*p3, *c, 1, 1]) 
        self.vertices.extend([*p4, *c, 0, 1])
    def add_quad_uv(self, p1, p2, p3, p4, uvs, color=(1,1,1,1)):
        c = list(color)
        self.vertices.extend([*p1, *c, *uvs[0]]) 
        self.vertices.extend([*p2, *c, *uvs[1]]) 
        self.vertices.extend([*p3, *c, *uvs[2]]) 
        self.vertices.extend([*p1, *c, *uvs[0]]) 
        self.vertices.extend([*p3, *c, *uvs[2]]) 
        self.vertices.extend([*p4, *c, *uvs[3]])
    def add_billboard(self, center, size, color, cam_right, cam_up):
        half = size * 0.5
        cx, cy, cz = center
        rx, ry, rz = cam_right * half
        ux, uy, uz = cam_up * half
        p1 = [cx - rx - ux, cy - ry - uy, cz - rz - uz] 
        p2 = [cx + rx - ux, cy + ry - uy, cz + rz - uz] 
        p3 = [cx + rx + ux, cy + ry + uy, cz + rz + uz] 
        p4 = [cx - rx + ux, cy - ry + uy, cz - rz + uz] 
        self.add_quad(p1, p2, p3, p4, color)
    def draw_ui_sprite(self, tex_id, x, y, w, h, proj_mat, color=(1,1,1,1)):
        self.vertices.clear()
        p1 = [x, y + h, 0]     
        p2 = [x + w, y + h, 0] 
        p3 = [x + w, y, 0]     
        p4 = [x, y, 0]         
        self.add_quad(p1, p2, p3, p4, color)
        view_identity = np.identity(4, dtype=np.float32)
        self.flush(view_identity, proj_mat, tex_id)
    def flush(self, view, proj, texture_id, mode=0):
        if not self.vertices: return
        self.shader.use()
        self.shader.set_mat4("view", view)
        self.shader.set_mat4("projection", proj)
        glUniform1i(glGetUniformLocation(self.shader.program, "uMode"), mode)
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, texture_id)
        glUniform1i(glGetUniformLocation(self.shader.program, "uTex"), 0)
        glBindVertexArray(self.vao)
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        data_np = np.array(self.vertices, dtype=np.float32)
        glBufferSubData(GL_ARRAY_BUFFER, 0, data_np.nbytes, data_np)
        count = len(self.vertices) // 9
        glDrawArrays(GL_TRIANGLES, 0, count)
        glBindVertexArray(0)
        self.vertices.clear()
    def delete(self):
        glDeleteBuffers(1, [self.vbo])
        glDeleteVertexArrays(1, [self.vao])
        self.shader.delete()
class BatchRenderer:
    def __init__(self, mode=GL_LINES):
        self.vertices = []  
        self.mode = mode    
        self.vbo = glGenBuffers(1)
        self.vao = glGenVertexArrays(1)
        self.max_vertices = 100000 
        self.shader = Shader("""
            #version 330 core
            layout (location = 0) in vec3 aPos;
            layout (location = 1) in vec4 aColor;
            uniform mat4 model;
            uniform mat4 view;
            uniform mat4 projection;
            out vec4 vColor;
            void main() {
                gl_Position = projection * view * model * vec4(aPos, 1.0);
                vColor = aColor;
            }
        """, """
            #version 330 core
            out vec4 FragColor;
            in vec4 vColor;
            void main() {
                FragColor = vColor;
            }
        """)
        glBindVertexArray(self.vao)
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        glBufferData(GL_ARRAY_BUFFER, self.max_vertices * 7 * 4, None, GL_DYNAMIC_DRAW)
        stride = 7 * 4
        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, stride, ctypes.c_void_p(0))
        glEnableVertexAttribArray(1)
        glVertexAttribPointer(1, 4, GL_FLOAT, GL_FALSE, stride, ctypes.c_void_p(12))
        glBindVertexArray(0)
    def _ensure_rgba(self, color):
        if len(color) == 3:
            return (*color, 1.0)
        return color
    def add_line(self, p1, p2, color=(1,1,1,1)):
        if self.mode != GL_LINES: return
        c = self._ensure_rgba(color) 
        self.vertices.extend([*p1, *c])
        self.vertices.extend([*p2, *c])
    def add_box(self, min_p, max_p, color=(1,1,1,1)):
        if self.mode != GL_LINES: return
        p0 = [min_p[0], min_p[1], min_p[2]]; p1 = [max_p[0], min_p[1], min_p[2]]
        p2 = [max_p[0], min_p[1], max_p[2]]; p3 = [min_p[0], min_p[1], max_p[2]]
        p4 = [min_p[0], max_p[1], min_p[2]]; p5 = [max_p[0], max_p[1], min_p[2]]
        p6 = [max_p[0], max_p[1], max_p[2]]; p7 = [min_p[0], max_p[1], max_p[2]]
        lines = [
            (p0, p1), (p1, p2), (p2, p3), (p3, p0),
            (p4, p5), (p5, p6), (p6, p7), (p7, p4),
            (p0, p4), (p1, p5), (p2, p6), (p3, p7)
        ]
        c = self._ensure_rgba(color) 
        for s, e in lines:
            self.vertices.extend([*s, *c])
            self.vertices.extend([*e, *c])
    def add_box_with_diagonals(self, min_p, max_p, color=(1,1,1,1)):
        if self.mode != GL_LINES: return
        x0, y0, z0 = min_p
        x1, y1, z1 = max_p
        p0 = [x0, y0, z0]; p1 = [x1, y0, z0]
        p2 = [x1, y1, z0]; p3 = [x0, y1, z0]
        p4 = [x0, y0, z1]; p5 = [x1, y0, z1]
        p6 = [x1, y1, z1]; p7 = [x0, y1, z1]
        c = self._ensure_rgba(color)
        pairs = [
            (p0, p1), (p1, p2), (p2, p3), (p3, p0),
            (p4, p5), (p5, p6), (p6, p7), (p7, p4),
            (p0, p4), (p1, p5), (p2, p6), (p3, p7),
            (p0, p2), (p1, p3), 
            (p4, p6), (p5, p7), 
            (p0, p5), (p1, p4), 
            (p3, p6), (p2, p7), 
            (p0, p7), (p3, p4), 
            (p1, p6), (p2, p5)  
        ]
        for s, e in pairs:
            self.vertices.extend([*s, *c])
            self.vertices.extend([*e, *c])
    def add_cube(self, center, size, color=(1,1,1,1)):
        if self.mode != GL_TRIANGLES: return
        dx, dy, dz = size[0]/2, size[1]/2, size[2]/2
        x, y, z = center
        p0 = [x-dx, y-dy, z+dz]; p1 = [x+dx, y-dy, z+dz]
        p2 = [x+dx, y+dy, z+dz]; p3 = [x-dx, y+dy, z+dz]
        p4 = [x+dx, y-dy, z-dz]; p5 = [x-dx, y-dy, z-dz]
        p6 = [x-dx, y+dy, z-dz]; p7 = [x+dx, y+dy, z-dz]
        c = list(self._ensure_rgba(color)) 
        def add_quad(v1, v2, v3, v4):
            self.vertices.extend([*v1, *c, *v2, *c, *v3, *c])
            self.vertices.extend([*v1, *c, *v3, *c, *v4, *c])
        add_quad(p0, p1, p2, p3)
        add_quad(p4, p5, p6, p7)
        add_quad(p5, p0, p3, p6)
        add_quad(p1, p4, p7, p2)
        add_quad(p3, p2, p7, p6)
        add_quad(p5, p4, p1, p0)
    def add_quad_2d(self, x, y, w, h, color=(1,1,1,1)):
        if self.mode != GL_TRIANGLES: return
        p1 = [x, y + h, 0]
        p2 = [x + w, y + h, 0]
        p3 = [x + w, y, 0]
        p4 = [x, y, 0]
        c = list(self._ensure_rgba(color)) 
        self.vertices.extend([*p1, *c, *p2, *c, *p3, *c])
        self.vertices.extend([*p1, *c, *p3, *c, *p4, *c])
    def flush(self, view_mat, proj_mat, line_width=1.0):
        if not self.vertices:
            return
        self.shader.use()
        model_mat = MatrixUtils.identity()
        self.shader.set_mat4("model", model_mat)
        self.shader.set_mat4("view", view_mat)
        self.shader.set_mat4("projection", proj_mat)
        glBindVertexArray(self.vao)
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        data_np = np.array(self.vertices, dtype=np.float32)
        glBufferSubData(GL_ARRAY_BUFFER, 0, data_np.nbytes, data_np)
        if self.mode == GL_LINES:
            glLineWidth(line_width)
        count = len(self.vertices) // 7
        glDrawArrays(self.mode, 0, count)
        glBindVertexArray(0)
        self.vertices.clear()
class TextureUtils:
    @staticmethod
    def preserve_texture_pos(old_ent, new_ent):
        diff = new_ent.pos - old_ent.pos
        old_s = old_ent.scale
        new_s = new_ent.scale
        new_uv_data = copy.deepcopy(new_ent.faces_uv_data)
        face_axes = [
            {'u': 2, 'v': 1, 'u_sgn': -1, 'v_sgn': 1},
            {'u': 2, 'v': 1, 'u_sgn': 1,  'v_sgn': 1},
            {'u': 0, 'v': 2, 'u_sgn': 1,  'v_sgn': -1},
            {'u': 0, 'v': 2, 'u_sgn': 1,  'v_sgn': 1},
            {'u': 0, 'v': 1, 'u_sgn': 1,  'v_sgn': 1},
            {'u': 0, 'v': 1, 'u_sgn': -1, 'v_sgn': 1},
        ]
        for i in range(6):
            mapping = face_axes[i]
            u_idx, v_idx = mapping['u'], mapping['v']
            data = new_uv_data[i]
            old_data = old_ent.faces_uv_data[i]
            rat_u = new_s[u_idx] / old_s[u_idx] if old_s[u_idx] > 1e-6 else 1.0
            rat_v = new_s[v_idx] / old_s[v_idx] if old_s[v_idx] > 1e-6 else 1.0
            if rat_u < 0.0001: rat_u = 1.0
            if rat_v < 0.0001: rat_v = 1.0
            rot = data['rot']
            if rot % 2 != 0:
                data['scl'][0] /= rat_v  
                data['scl'][1] /= rat_u  
            else:
                data['scl'][0] /= rat_u
                data['scl'][1] /= rat_v
            delta_pos_u = diff[u_idx] * mapping['u_sgn']
            delta_pos_v = diff[v_idx] * mapping['v_sgn']
            shift_u = delta_pos_u / old_s[u_idx] if old_s[u_idx] > 1e-6 else 0.0
            shift_v = delta_pos_v / old_s[v_idx] if old_s[v_idx] > 1e-6 else 0.0
            data['off'][0] = (old_data['off'][0] - shift_u) / rat_u
            data['off'][1] = (old_data['off'][1] - shift_v) / rat_v
        new_ent.faces_uv_data = new_uv_data
    @staticmethod
    def adjust_uvs_after_move(old_ent, new_ent):
        TextureUtils.preserve_texture_pos(old_ent, new_ent)
    @staticmethod
    def rotate_entity_data(ent, axis, direction=1):
        if axis == 1: 
            perm = [4, 5, 2, 3, 1, 0] 
        elif axis == 0: 
            perm = [0, 1, 5, 4, 2, 3] 
        elif axis == 2: 
            perm = [3, 2, 0, 1, 4, 5]
        else:
            return
        if direction == -1:
            rev_perm = [0]*6
            for i, p in enumerate(perm):
                rev_perm[p] = i
            perm = rev_perm
        def apply_perm(arr):
            return [copy.deepcopy(arr[p]) for p in perm]
        ent.faces_colors = apply_perm(ent.faces_colors)
        ent.faces_textures = apply_perm(ent.faces_textures)
        ent.faces_tiling = apply_perm(ent.faces_tiling)
        ent.faces_uv_data = apply_perm(ent.faces_uv_data)
        ent.faces_reflectivity = apply_perm(ent.faces_reflectivity) 
        faces_to_rotate_uv = []
        if axis == 1: faces_to_rotate_uv = [2, 3] 
        elif axis == 0: faces_to_rotate_uv = [0, 1] 
        elif axis == 2: faces_to_rotate_uv = [4, 5] 
        for f_idx in faces_to_rotate_uv:
            ent.faces_uv_data[f_idx]['rot'] = (ent.faces_uv_data[f_idx]['rot'] - direction) % 4
    @staticmethod
    def mirror_entity_data(ent, axis):
        perm = list(range(6))
        if axis == 0: 
            perm[0], perm[1] = 1, 0
            faces_to_flip = [2, 3, 4, 5]
        elif axis == 1: 
            perm[2], perm[3] = 3, 2
            faces_to_flip = [0, 1, 4, 5]
        elif axis == 2: 
            perm[4], perm[5] = 5, 4
            faces_to_flip = [0, 1, 2, 3]
        def apply_perm(arr):
            return [copy.deepcopy(arr[p]) for p in perm]
        ent.faces_colors = apply_perm(ent.faces_colors)
        ent.faces_textures = apply_perm(ent.faces_textures)
        ent.faces_tiling = apply_perm(ent.faces_tiling)
        ent.faces_uv_data = apply_perm(ent.faces_uv_data)
        ent.faces_reflectivity = apply_perm(ent.faces_reflectivity)
        for f_idx in faces_to_flip:
            ent.faces_uv_data[f_idx]['fliph'] = 1 - ent.faces_uv_data[f_idx]['fliph']
class ChunkMeshBuilder:
    @staticmethod
    def build_chunk_data(entities, chunk_coord, texture_manager):
        # Ключ теперь: (tex_id, mode, is_transparent)
        batches = {} 
        white_tex_id = texture_manager.get_white_texture()
        
        for ent in entities:
            if ent.is_hole or ent.is_animating: continue 
            
            x, y, z = ent.pos
            uid_val = int(ent.uid[:4], 16) if ent.uid else 0
            noise = (uid_val % 100) * 0.000005 
            major_expand = 0.001 + noise 
            minor_expand = 0.00005 + (noise * 0.1)
            s = ent.scale
            min_dim_idx = np.argmin(s) 
            final_scale = np.array(s, copy=True)
            for i in range(3):
                if i == min_dim_idx: final_scale[i] += major_expand
                else: final_scale[i] += minor_expand
            dx, dy, dz = final_scale[0]/2.0, final_scale[1]/2.0, final_scale[2]/2.0
            
            pb1 = [x - dx, y - dy, z + dz]
            pb2 = [x + dx, y - dy, z + dz]
            pb3 = [x + dx, y - dy, z - dz]
            pb4 = [x - dx, y - dy, z - dz]
            pt1 = [x - dx, y + dy, z + dz]
            pt2 = [x + dx, y + dy, z + dz]
            pt3 = [x + dx, y + dy, z - dz]
            pt4 = [x - dx, y + dy, z - dz]
            
            ao_factor = ent.brightness 
            
            def add_face(c1, c2, c3, c4, normal, c_idx):
                tex_path = ent.faces_textures[c_idx]
                tex_id = None
                target_tex_id = white_tex_id
                target_mode = 0 
                
                if tex_path:
                    found_id = texture_manager.load_from_file(tex_path)
                    if found_id is not None:
                        tex_id = found_id
                        target_tex_id = tex_id
                        target_mode = 2 if ent.faces_tiling[c_idx] else 1
                
                col = ent.faces_colors[c_idx]
                base_alpha = col[3] if len(col) > 3 else 1.0
                
                # Поддержка прозрачности (из предыдущего фикса)
                is_transparent = (base_alpha < 0.99) or (ent.density < 0.99)
                batch_key = (target_tex_id, target_mode, is_transparent)
                
                if batch_key not in batches:
                    batches[batch_key] = []
                target_list = batches[batch_key]
                
                r = col[0] * ao_factor
                g = col[1] * ao_factor
                b = col[2] * ao_factor
                a = base_alpha 
                
                emission = col[4] if len(col) > 4 else 0.0
                gloss = col[5] if len(col) > 5 else 0.0
                reflect = ent.faces_reflectivity[c_idx] if hasattr(ent, 'faces_reflectivity') else 0.0
                
                nx, ny, nz = normal
                
                face_aspect = 1.0
                if c_idx in [0, 1]: 
                    if final_scale[1] > 0.001: face_aspect = final_scale[2] / final_scale[1]
                elif c_idx in [2, 3]: 
                    if final_scale[2] > 0.001: face_aspect = final_scale[0] / final_scale[2]
                elif c_idx in [4, 5]: 
                    if final_scale[1] > 0.001: face_aspect = final_scale[0] / final_scale[1]
                
                # --- ЛОГИКА UV ---
                u1, v1, u2, v2, u3, v3, u4, v4 = 0,0,0,0,0,0,0,0

                if tex_id is not None:
                    # == Если есть текстура: используем локальные UV (как раньше) ==
                    raw_uvs = [
                        np.array([0.0, 0.0]), np.array([1.0, 0.0]),
                        np.array([1.0, 1.0]), np.array([0.0, 1.0])
                    ]
                    uv_data = ent.faces_uv_data[c_idx]
                    off_x, off_y = uv_data['off']
                    scl_x, scl_y = uv_data['scl']
                    rot = uv_data['rot']
                    flip_h = uv_data['fliph']
                    flip_v = uv_data['flipv']
                    
                    if rot % 2 != 0:
                        scl_x, scl_y = scl_y, scl_x
                    
                    final_uvs = []
                    for uv in raw_uvs:
                        curr = uv - 0.5
                        curr[0] -= off_x
                        curr[1] -= off_y
                        if abs(scl_x) > 0.0001: curr[0] /= scl_x
                        if abs(scl_y) > 0.0001: curr[1] /= scl_y
                        if flip_h: curr[0] = -curr[0]
                        if flip_v: curr[1] = -curr[1]
                        
                        curr[0] *= face_aspect
                        if rot == 1:   curr = np.array([-curr[1], curr[0]])
                        elif rot == 2: curr = np.array([-curr[0], -curr[1]])
                        elif rot == 3: curr = np.array([curr[1], -curr[0]])
                        
                        if face_aspect > 0.0001:
                            curr[0] /= face_aspect
                        curr += 0.5
                        final_uvs.append(curr)
                    
                    u1, v1 = final_uvs[0]
                    u2, v2 = final_uvs[1]
                    u3, v3 = final_uvs[2]
                    u4, v4 = final_uvs[3]
                else:
                    # == Если нет текстуры (цвет + шум): ИСПОЛЬЗУЕМ МИРОВЫЕ КООРДИНАТЫ ==
                    # Это "прибивает" шум к координатам мира, а не к углу объекта.
                    # При разрезании координаты вершин остаются теми же -> шум не дергается.
                    
                    noise_scale = 0.03 # Коэффициент плотности шума
                    
                    def get_world_uv(pt, f_idx):
                        # pt = [x, y, z] - реальная координата вершины
                        if f_idx in [0, 1]: # Бока (ось X) -> берем Z и Y
                            return pt[2] * noise_scale, pt[1] * noise_scale
                        elif f_idx in [2, 3]: # Верх/Низ (ось Y) -> берем X и Z
                            return pt[0] * noise_scale, pt[2] * noise_scale
                        elif f_idx in [4, 5]: # Перед/Зад (ось Z) -> берем X и Y
                            return pt[0] * noise_scale, pt[1] * noise_scale
                        return 0.0, 0.0

                    u1, v1 = get_world_uv(c1, c_idx)
                    u2, v2 = get_world_uv(c2, c_idx)
                    u3, v3 = get_world_uv(c3, c_idx)
                    u4, v4 = get_world_uv(c4, c_idx)
                
                target_list.extend([c1[0], c1[1], c1[2], r, g, b, a, nx, ny, nz, u1, v1, emission, gloss, reflect]) 
                target_list.extend([c2[0], c2[1], c2[2], r, g, b, a, nx, ny, nz, u2, v2, emission, gloss, reflect]) 
                target_list.extend([c3[0], c3[1], c3[2], r, g, b, a, nx, ny, nz, u3, v3, emission, gloss, reflect]) 
                target_list.extend([c1[0], c1[1], c1[2], r, g, b, a, nx, ny, nz, u1, v1, emission, gloss, reflect]) 
                target_list.extend([c3[0], c3[1], c3[2], r, g, b, a, nx, ny, nz, u3, v3, emission, gloss, reflect]) 
                target_list.extend([c4[0], c4[1], c4[2], r, g, b, a, nx, ny, nz, u4, v4, emission, gloss, reflect]) 
            
            add_face(pb1, pb2, pt2, pt1, [0, 0, 1], 4)
            add_face(pb3, pb4, pt4, pt3, [0, 0, -1], 5)
            add_face(pt1, pt2, pt3, pt4, [0, 1, 0], 2)
            add_face(pb4, pb3, pb2, pb1, [0, -1, 0], 3)
            add_face(pb2, pb3, pt3, pt2, [1, 0, 0], 0)
            add_face(pb4, pb1, pt1, pt4, [-1, 0, 0], 1)
            
        final_batches = {}
        for key, data in batches.items():
            if data:
                final_batches[key] = np.array(data, dtype=np.float32)
        return final_batches
DEFAULT_VERT_SHADER = """
#version 330 core
layout (location = 0) in vec3 aPos;
layout (location = 1) in vec4 aColor;
layout (location = 2) in vec3 aNormal;
layout (location = 3) in vec2 aTexCoord;
layout (location = 4) in float aEmission;
layout (location = 5) in float aGloss;
layout (location = 6) in float aReflect;
uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;
uniform int useWorldUV; 
uniform float uvScale;
uniform vec4 uClipPlane; // <--- Плоскость отсечения
out vec3 FragPos;
out vec4 vColor;
out vec3 Normal;
out vec2 TexCoord;
out float vEmission;
out float vGloss;
out float vReflect;
void main()
{
    vec4 worldPos = model * vec4(aPos, 1.0);
    // --- CLIPPING (Обрезаем всё, что за зеркалом) ---
    gl_ClipDistance[0] = dot(worldPos, uClipPlane);
    FragPos = vec3(worldPos);
    Normal = mat3(transpose(inverse(model))) * aNormal;
    vColor = aColor;
    vEmission = aEmission;
    vGloss = aGloss;
    vReflect = aReflect;
    if (useWorldUV == 1) {
        TexCoord = vec2(worldPos.x, worldPos.z) * uvScale;
    } else {
        TexCoord = aTexCoord;
    }
    gl_Position = projection * view * worldPos;
}
"""
_ref_logic = ""
for i in range(MAX_MIRRORS):
    _ref_logic += "else if (i == " + str(i) + ") reflectionColor = texture(uTexReflections[" + str(i) + "], screenUV).rgb; "
DEFAULT_FRAG_SHADER = """
#version 330 core
#define MAX_MIRRORS """ + str(MAX_MIRRORS) + """
out vec4 FragColor;
in vec3 FragPos;
in vec4 vColor;
in vec3 Normal;
in vec2 TexCoord;
in float vEmission; 
in float vGloss;
in float vReflect; // Степень зеркальности (0..1)
// Текстуры
uniform sampler2D uTexMain;       // Основная текстура (Slot 0)
uniform sampler2D uTexNoise;      // Шум (Slot 1)
// Массив текстур для зеркал (Slots 2..2+MAX_MIRRORS)
uniform sampler2D uTexReflections[MAX_MIRRORS]; // MAX_MIRRORS = 4
// Настройки
uniform int uTexType;        // 0=Color+Noise, 1=Texture(Clamp)+Noise, 2=Texture(Repeat)
uniform vec2 uWindowSize;    // Размер окна для расчета UV экрана
uniform int uReflectionMode; // 0=Fake(Metal), 1=Real(FBO)
// Данные для выбора зеркала
uniform int uActiveMirrors;
uniform vec3 uMirrorPos[MAX_MIRRORS];
uniform vec3 uMirrorNormal[MAX_MIRRORS];
// Камера и Свет
uniform vec3 viewPos;
uniform vec3 sunDirection;
uniform vec3 sunColor;
uniform vec3 ambientColor;
uniform float lightIntensity;
// Точечные источники
struct PointLight {
    vec3 position;
    vec3 color;
    float constant;
    float linear;
    float quadratic;
};
#define NR_POINT_LIGHTS 64 
uniform PointLight pointLights[NR_POINT_LIGHTS];
uniform int numLights;
// Туман
uniform vec3 fogColor;
uniform float fogStart;
uniform float fogEnd;
void main() {
    vec3 norm = normalize(Normal);
    vec3 viewDir = normalize(viewPos - FragPos);
    vec4 baseColorRGBA = vColor;
    // --- 1. ТЕКСТУРИРОВАНИЕ (ВОССТАНОВЛЕННАЯ ЛОГИКА) ---
    bool applyTexture = false;
    if (uTexType == 1) {
        // Режим 1: Текстура накладывается только внутри 0..1 (для картин на стенах)
        // Используем 0.001 и 0.999 чтобы убрать артефакты на краях
        if (TexCoord.x >= 0.001 && TexCoord.x <= 0.999 && 
            TexCoord.y >= 0.001 && TexCoord.y <= 0.999) {
            vec4 texVal = texture(uTexMain, TexCoord);
            baseColorRGBA *= texVal;
            applyTexture = true;
        }
    } 
    else if (uTexType == 2) {
        // Режим 2: Тайлинг (плитка, обои)
        vec4 texVal = texture(uTexMain, TexCoord);
        baseColorRGBA *= texVal;
        applyTexture = true;
    }
    // Если текстуры нет (или мы вышли за границы в режиме 1) -> Применяем Шум
    if (!applyTexture) {
        vec2 noiseUV = TexCoord;
        // Если это режим "картины", но мы за ее пределами - увеличиваем частоту шума
        if (uTexType == 1) {
             noiseUV *= 10.0; 
        }
        vec4 noiseVal = texture(uTexNoise, noiseUV);
        // Мягкое смешивание цвета с шумом (как было раньше)
        vec3 noisyColor = baseColorRGBA.rgb * noiseVal.rgb;
        baseColorRGBA.rgb = mix(baseColorRGBA.rgb, noisyColor, 0.3);
    }
    if(baseColorRGBA.a < 0.01) discard;
    vec3 albedo = baseColorRGBA.rgb;
    // --- 2. ОСВЕЩЕНИЕ (Sun + Points) ---
    // Солнце
    vec3 sunDirNorm = normalize(sunDirection);
    float sunDiff = max(dot(norm, sunDirNorm), 0.0);
    float sunSpec = 0.0;
    if (vGloss > 0.01 && sunDiff > 0.0) {
        vec3 halfwayDir = normalize(sunDirNorm + viewDir);
        sunSpec = pow(max(dot(norm, halfwayDir), 0.0), 32.0) * vGloss;
    }
    vec3 ambient = ambientColor * albedo;
    vec3 sunDiffuse = sunColor * sunDiff * lightIntensity * albedo;
    vec3 sunSpecular = sunColor * sunSpec * lightIntensity; 
    // Точечные источники
    vec3 pointDiffuseTotal = vec3(0.0);
    vec3 pointSpecularTotal = vec3(0.0);
    for(int i = 0; i < numLights; i++) {
        vec3 lightDir = normalize(pointLights[i].position - FragPos);
        float dist = length(pointLights[i].position - FragPos);
        // Формула затухания света
        float att = 1.0 / (pointLights[i].constant + pointLights[i].linear * dist + pointLights[i].quadratic * (dist * dist));
        float diff = max(dot(norm, lightDir), 0.0);
        float spec = 0.0;
        if(vGloss > 0.01 && diff > 0.0) {
             vec3 halfDir = normalize(lightDir + viewDir);
             spec = pow(max(dot(norm, halfDir), 0.0), 32.0) * vGloss;
        }
        pointDiffuseTotal += pointLights[i].color * diff * att;
        pointSpecularTotal += pointLights[i].color * spec * att;
    }
    // Суммарный свет (без отражений)
    vec3 diffuseTotal = sunDiffuse + pointDiffuseTotal * albedo;
    vec3 specularTotal = sunSpecular + pointSpecularTotal;
    vec3 emissionLight = albedo * vEmission * 1.5; 
    vec3 result = ambient + diffuseTotal + specularTotal + emissionLight;
    // --- 3. ЗЕРКАЛЬНОСТЬ (REFLECTIONS) ---
    if (vReflect > 0.01) {
        vec3 reflectionColor;
        bool foundMirror = false;
        if (uReflectionMode == 1) {
            // === РЕЖИМ 1: ЧЕСТНОЕ ЗЕРКАЛО (FBO) ===
            vec2 screenUV = gl_FragCoord.xy / uWindowSize;
            // Ищем ближайшее зеркало
            for(int i=0; i<uActiveMirrors; i++) {
                float dist = abs(dot(FragPos - uMirrorPos[i], uMirrorNormal[i]));
                // Добавлена проверка align: нормаль пикселя должна совпадать с нормалью зеркала
                float align = dot(norm, uMirrorNormal[i]);
                if(dist < 0.15 && align > 0.9) { 
                    if (false) {} """ + _ref_logic + """
                    reflectionColor *= 0.9;
                    foundMirror = true;
                    break;
                }
            }
        }
        if (!foundMirror) {
            // === РЕЖИМ 0: ИМИТАЦИЯ (МЕТАЛЛ/НЕБО) ===
            // Используется, если зеркало перекрыто или далеко
            vec3 I = normalize(FragPos - viewPos);
            vec3 R = reflect(I, norm);
            if (R.y > 0.0) {
                // Отражаем небо
                float skyGradient = pow(R.y, 0.5);
                // Если день - берем цвет тумана, если ночь - темноту
                vec3 skyTop = (length(fogColor) > 0.1) ? fogColor * 0.8 : vec3(0.05, 0.05, 0.1);
                reflectionColor = mix(fogColor, skyTop, skyGradient);
                // Блик солнца на металле
                float sunDot = dot(R, sunDirNorm);
                if (sunDot > 0.95) {
                    reflectionColor += sunColor * smoothstep(0.95, 0.98, sunDot) * 2.0;
                }
            } else {
                // Отражаем землю (темная)
                reflectionColor = vec3(0.1, 0.15, 0.1) * lightIntensity;
            }
        }
        // Смешиваем основной цвет объекта с отражением
        // vReflect: 0 = только цвет, 1 = только отражение
        // Умножаем на 0.8, чтобы даже 100% зеркало сохраняло немного "тела" объекта, или убери 0.8 для идеального зеркала
        result = mix(result, reflectionColor, vReflect * 0.9);
    }
    // --- 4. ТУМАН ---
    float distance = length(viewPos - FragPos);
    float fogFactor = (fogEnd - distance) / (fogEnd - fogStart);
    fogFactor = clamp(fogFactor, 0.0, 1.0);
    vec3 finalColor = mix(fogColor, result, fogFactor);
    FragColor = vec4(finalColor, baseColorRGBA.a);
}
"""
class Shader:
    def __init__(self, vert_source, frag_source):
        self.program = glCreateProgram()
        vs = self._compile_shader(vert_source, GL_VERTEX_SHADER)
        fs = self._compile_shader(frag_source, GL_FRAGMENT_SHADER)
        if not vs or not fs:
            print("Shader compilation failed.")
            return
        glAttachShader(self.program, vs)
        glAttachShader(self.program, fs)
        glLinkProgram(self.program)
        if glGetProgramiv(self.program, GL_LINK_STATUS) != GL_TRUE:
            info = glGetProgramInfoLog(self.program)
            print(f"Shader Link Error: {info}")
        glDeleteShader(vs)
        glDeleteShader(fs)
    def _compile_shader(self, source, shader_type):
        shader = glCreateShader(shader_type)
        glShaderSource(shader, source)
        glCompileShader(shader)
        if glGetShaderiv(shader, GL_COMPILE_STATUS) != GL_TRUE:
            info = glGetShaderInfoLog(shader)
            print(f"Shader Compile Error ({'VERT' if shader_type==GL_VERTEX_SHADER else 'FRAG'}): {info}")
            glDeleteShader(shader)
            return None
        return shader
    def use(self):
        glUseProgram(self.program)
    def set_mat4(self, name, mat):
        loc = glGetUniformLocation(self.program, name)
        glUniformMatrix4fv(loc, 1, GL_TRUE, mat)
    def delete(self):
        glDeleteProgram(self.program)
class MeshBuffer:
    def __init__(self, data_array):
        self.vertex_count = len(data_array) // 15  
        self.vao = glGenVertexArrays(1)
        self.vbo = glGenBuffers(1)
        glBindVertexArray(self.vao)
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        glBufferData(GL_ARRAY_BUFFER, data_array.nbytes, data_array, GL_STATIC_DRAW)
        stride = 60 
        glEnableVertexAttribArray(0); glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, stride, ctypes.c_void_p(0))
        glEnableVertexAttribArray(1); glVertexAttribPointer(1, 4, GL_FLOAT, GL_FALSE, stride, ctypes.c_void_p(12))
        glEnableVertexAttribArray(2); glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE, stride, ctypes.c_void_p(28))
        glEnableVertexAttribArray(3); glVertexAttribPointer(3, 2, GL_FLOAT, GL_FALSE, stride, ctypes.c_void_p(40))
        glEnableVertexAttribArray(4); glVertexAttribPointer(4, 1, GL_FLOAT, GL_FALSE, stride, ctypes.c_void_p(48))
        glEnableVertexAttribArray(5); glVertexAttribPointer(5, 1, GL_FLOAT, GL_FALSE, stride, ctypes.c_void_p(52))
        glEnableVertexAttribArray(6)
        glVertexAttribPointer(6, 1, GL_FLOAT, GL_FALSE, stride, ctypes.c_void_p(56))
        glBindVertexArray(0)
    def draw(self):
        if self.vertex_count > 0:
            glBindVertexArray(self.vao)
            glDrawArrays(GL_TRIANGLES, 0, self.vertex_count)
            glBindVertexArray(0)
    def delete(self):
        glDeleteBuffers(1, [self.vbo])
        glDeleteVertexArrays(1, [self.vao])
class InputManager:
    def __init__(self):
        self.keys = {}
        self.mouse_pos = (0, 0)
        self.mouse_rel = (0, 0)
        self.mouse_buttons = {1: False, 2: False, 3: False}
        self.mouse_wheel_y = 0
    def process_event(self, event):
        if event.type == sdl2.SDL_MOUSEMOTION:
            self.mouse_pos = (event.motion.x, event.motion.y)
            self.mouse_rel = (self.mouse_rel[0] + event.motion.xrel, 
                              self.mouse_rel[1] + event.motion.yrel)
        elif event.type == sdl2.SDL_MOUSEBUTTONDOWN:
            btn = event.button.button
            if btn == sdl2.SDL_BUTTON_LEFT: self.mouse_buttons[1] = True
            elif btn == sdl2.SDL_BUTTON_MIDDLE: self.mouse_buttons[2] = True
            elif btn == sdl2.SDL_BUTTON_RIGHT: self.mouse_buttons[3] = True
        elif event.type == sdl2.SDL_MOUSEBUTTONUP:
            btn = event.button.button
            if btn == sdl2.SDL_BUTTON_LEFT: self.mouse_buttons[1] = False
            elif btn == sdl2.SDL_BUTTON_MIDDLE: self.mouse_buttons[2] = False
            elif btn == sdl2.SDL_BUTTON_RIGHT: self.mouse_buttons[3] = False
        elif event.type == sdl2.SDL_MOUSEWHEEL:
            self.mouse_wheel_y = event.wheel.y
        elif event.type == sdl2.SDL_KEYDOWN:
            self.keys[event.key.keysym.sym] = True
        elif event.type == sdl2.SDL_KEYUP:
            self.keys[event.key.keysym.sym] = False
    def reset_per_frame(self):
        self.mouse_rel = (0, 0)
        self.mouse_wheel_y = 0
    def get_keys(self):
        return self.keys
    def get_mouse_pos(self):
        return self.mouse_pos
    def get_mouse_rel(self):
        return self.mouse_rel
def safe_text_to_texture(text, font, color=(255, 255, 255)):
    if not text: return None, 0, 0
    try:
        base_surf = font.render(text, True, color)
        w, h = base_surf.get_width(), base_surf.get_height()
        if w == 0 or h == 0: return None, 0, 0
        final_surf = pygame.Surface((w + 2, h + 2), pygame.SRCALPHA)
        final_surf.fill((0,0,0,0)) 
        outline_surf = font.render(text, True, (70, 70, 70))
        for dx, dy in [(-1, -1), (1, -1), (-1, 1), (1, 1), (0, -1), (0, 1), (-1, 0), (1, 0)]:
             final_surf.blit(outline_surf, (dx+2, dy+2)) 
        final_surf.blit(base_surf, (2, 2))
        fw, fh = final_surf.get_width(), final_surf.get_height()
        text_data = pygame.image.tostring(final_surf, "RGBA", True)
        tex_id = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, tex_id)
        glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, fw, fh, 0, GL_RGBA, GL_UNSIGNED_BYTE, text_data)
        glBindTexture(GL_TEXTURE_2D, 0)
        return tex_id, fw, fh
    except Exception as e:
        print(f"Texture Error: {e}")
        return None, 0, 0
def upload_texture_to_gpu(surface, wrap_mode=GL_CLAMP_TO_EDGE):
    w, h = surface.get_width(), surface.get_height()
    texture_data = pygame.image.tostring(surface, "RGBA", True)
    tex_id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, tex_id)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, w, h, 0, GL_RGBA, GL_UNSIGNED_BYTE, texture_data)
    glGenerateMipmap(GL_TEXTURE_2D)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, wrap_mode)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, wrap_mode)
    glBindTexture(GL_TEXTURE_2D, 0)
    return tex_id
def create_circle_texture(color, size=512, hardness=0.5, noise_strength=0.0):
    x = np.linspace(-1, 1, size)
    y = np.linspace(-1, 1, size)
    X, Y = np.meshgrid(x, y)
    dist = np.sqrt(X**2 + Y**2)
    max_radius = 0.95
    core_radius = max_radius * hardness
    alpha_gradient = np.clip((max_radius - dist) / (max_radius - core_radius), 0.0, 1.0)
    alpha_gradient = alpha_gradient * alpha_gradient * (3.0 - 2.0 * alpha_gradient)
    base_alpha = color[3] if len(color) > 3 else 255
    img = np.zeros((size, size, 4), dtype=np.uint8)
    if noise_strength > 0:
        noise_res = 10
        noise_raw = np.random.randint(120, 256, (noise_res, noise_res), dtype=np.uint8)
        surf_noise = pygame.Surface((noise_res, noise_res))
        noise_rgb = np.dstack((noise_raw, noise_raw, noise_raw))
        pygame.surfarray.blit_array(surf_noise, noise_rgb)
        step1 = pygame.transform.smoothscale(surf_noise, (128, 128))
        step2 = pygame.transform.smoothscale(step1, (32, 32)) 
        surf_final = pygame.transform.smoothscale(step2, (size, size))
        arr_final = pygame.surfarray.array3d(surf_final)
        noise_norm = arr_final.astype(np.float32) / 255.0
        blend = 0.65 + (noise_norm * 0.35)
        img[:,:,0] = (color[0] * blend[:,:,0]).astype(np.uint8)
        img[:,:,1] = (color[1] * blend[:,:,1]).astype(np.uint8)
        img[:,:,2] = (color[2] * blend[:,:,2]).astype(np.uint8)
    else:
        img[:,:,0] = color[0]
        img[:,:,1] = color[1]
        img[:,:,2] = color[2]
    img[:,:,3] = (alpha_gradient * base_alpha).astype(np.uint8)
    tex_id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, tex_id)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, size, size, 0, GL_RGBA, GL_UNSIGNED_BYTE, img.tobytes())
    glGenerateMipmap(GL_TEXTURE_2D)
    return tex_id
def create_light_icon_texture():
    size = 128
    surf = pygame.Surface((size, size), pygame.SRCALPHA)
    surf.fill((0, 0, 0, 0)) 
    color_circle = (255, 255, 200, 180)
    color_dot = (255, 255, 255, 255)
    center = (size // 2, size // 2)
    radius = (size // 2) - 4 
    pygame.draw.circle(surf, color_circle, center, radius, 4)
    pygame.draw.circle(surf, color_dot, center, 8)
    return upload_texture_to_gpu(surf, GL_CLAMP_TO_EDGE)
def create_grid_texture_pattern():
    size = 64
    surf = pygame.Surface((size, size), pygame.SRCALPHA)
    surf.fill((0, 0, 0, 0)) 
    color = (255, 255, 255, 100) 
    thickness = 2
    pygame.draw.rect(surf, color, (0, 0, size, size), thickness)
    return upload_texture_to_gpu(surf, GL_REPEAT)
def create_procedural_cloud_texture():
    size = 1024
    base_size = 128
    surf_base = pygame.Surface((base_size, base_size))
    rand_array = np.random.randint(0, 255, (base_size, base_size, 3), dtype=np.uint8)
    pygame.surfarray.blit_array(surf_base, rand_array)
    surf_base = pygame.transform.smoothscale(surf_base, (size, size))
    detail_size = 512
    surf_detail = pygame.Surface((detail_size, detail_size))
    rand_array_d = np.random.randint(0, 255, (detail_size, detail_size, 3), dtype=np.uint8)
    pygame.surfarray.blit_array(surf_detail, rand_array_d)
    surf_detail = pygame.transform.smoothscale(surf_detail, (size, size))
    arr_base = pygame.surfarray.array3d(surf_base).astype(np.float32)
    arr_detail = pygame.surfarray.array3d(surf_detail).astype(np.float32)
    noise_val = (arr_base[:,:,0] * 0.70 + arr_detail[:,:,0] * 0.30)
    res_img = np.zeros((size, size, 4), dtype=np.uint8)
    res_img[:,:,0] = 255 
    res_img[:,:,1] = 255 
    res_img[:,:,2] = 255 
    normalized = noise_val / 255.0
    min_threshold = 0.30 
    alpha = np.clip((normalized - min_threshold) / (1.0 - min_threshold), 0.0, 1.0)
    alpha = np.power(alpha, 1.2)
    final_alpha = alpha * 250.0
    res_img[:,:,3] = final_alpha.astype(np.uint8)
    tex_id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, tex_id)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    texture_data = res_img.transpose(1, 0, 2).tobytes()
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, size, size, 0, GL_RGBA, GL_UNSIGNED_BYTE, texture_data)
    glGenerateMipmap(GL_TEXTURE_2D)
    return tex_id
def create_noise_texture():
    width, height = 128, 128
    low = 225
    high = 256
    noise_vals = np.random.randint(low, high, (width, height), dtype=np.uint8)
    data = np.zeros((width, height, 4), dtype=np.uint8)
    data[:, :, 0] = noise_vals
    data[:, :, 1] = noise_vals
    data[:, :, 2] = noise_vals
    data[:, :, 3] = 255 
    texture_data = data.tobytes()
    tex_id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, tex_id)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, texture_data)
    return tex_id
class Widget:
    def __init__(self, x, y, w, h):
        self.rect = pygame.Rect(x, y, w, h)
        self.hovered = False
    def delete(self):
        if hasattr(self, 'tex'):
            glDeleteTextures([self.tex])
            del self.tex
    def check_hover(self, mx, my):
        self.hovered = self.rect.collidepoint(mx, my)
        return self.hovered
    def draw_rect(self, color):
        glColor4f(*color)
        glBegin(GL_QUADS)
        glVertex2f(self.rect.x, self.rect.y)
        glVertex2f(self.rect.x + self.rect.w, self.rect.y)
        glVertex2f(self.rect.x + self.rect.w, self.rect.y + self.rect.h)
        glVertex2f(self.rect.x, self.rect.y + self.rect.h)
        glEnd()
class Button(Widget):
    def __init__(self, x, y, w, h, text, font, callback):
        super().__init__(x, y, w, h)
        self.text = text
        self.font = font
        self.callback = callback
        self.tex, self.tw, self.th = safe_text_to_texture(text, font)
    def draw(self):
        col = (0.3, 0.3, 0.3, 0.8) if self.hovered else (0.2, 0.2, 0.2, 0.8)
        self.draw_rect(col)
        if not hasattr(self, 'tex'): return
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, self.tex)
        glColor4f(1, 1, 1, 1)
        tx = self.rect.x + (self.rect.w - self.tw) // 2
        ty = self.rect.y + (self.rect.h - self.th) // 2
        glBegin(GL_QUADS)
        glTexCoord2f(0, 0); glVertex2f(tx, ty + self.th)
        glTexCoord2f(1, 0); glVertex2f(tx + self.tw, ty + self.th)
        glTexCoord2f(1, 1); glVertex2f(tx + self.tw, ty)
        glTexCoord2f(0, 1); glVertex2f(tx, ty)
        glEnd()
        glDisable(GL_TEXTURE_2D)
        glDisable(GL_BLEND)
    def click(self):
        if self.callback: self.callback()
class TextLabel:
    def __init__(self, font, color=(255, 255, 255)):
        self.font = font
        self.color = color
        self.tex = None
        self.w = 0
        self.h = 0
        self.current_text = None
    def set_text(self, text):
        if text == self.current_text:
            return
        self.current_text = text
        if self.tex:
            glBindTexture(GL_TEXTURE_2D, 0) 
            glDeleteTextures([self.tex])
            self.tex = None
        self.tex, self.w, self.h = safe_text_to_texture(text, self.font, self.color)
    def draw(self, x, y):
        if not self.tex: return
        glPushAttrib(GL_CURRENT_BIT | GL_ENABLE_BIT | GL_TEXTURE_BIT)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, self.tex)
        glColor4f(1, 1, 1, 1) 
        glBegin(GL_QUADS)
        glTexCoord2f(0, 0); glVertex2f(x, y + self.h)
        glTexCoord2f(1, 0); glVertex2f(x + self.w, y + self.h)
        glTexCoord2f(1, 1); glVertex2f(x + self.w, y)
        glTexCoord2f(0, 1); glVertex2f(x, y)
        glEnd()
        glBindTexture(GL_TEXTURE_2D, 0)
        glPopAttrib()
    def delete(self):
        if self.tex:
            glBindTexture(GL_TEXTURE_2D, 0)
            glDeleteTextures([self.tex])
            self.tex = None
class Slider(Widget):
    def __init__(self, x, y, w, h, min_val, max_val, initial, label, font):
        super().__init__(x, y, w, h)
        self.min_val = min_val
        self.max_val = max_val
        self.value = initial
        self.label = label
        self.font = font
        self.dragging = False
        self.update_texture()
    def update_texture(self):
        if hasattr(self, 'tex'):
            glDeleteTextures([self.tex])
        val_str = f"{self.value:.2f}" if self.max_val < 10 else f"{int(self.value)}"
        txt = f"{self.label}: {val_str}"
        self.tex, self.tw, self.th = safe_text_to_texture(txt, self.font)
    def handle_event(self, event):
        if event.type == sdl2.SDL_MOUSEBUTTONDOWN:
            if event.button.button == sdl2.SDL_BUTTON_LEFT:
                mx, my = event.button.x, event.button.y
                if self.rect.collidepoint(mx, my):
                    self.dragging = True
                    self.update_value(mx)
                    return True
        elif event.type == sdl2.SDL_MOUSEBUTTONUP:
            if event.button.button == sdl2.SDL_BUTTON_LEFT:
                self.dragging = False
        elif event.type == sdl2.SDL_MOUSEMOTION:
            if self.dragging:
                mx = event.motion.x
                self.update_value(mx)
                return True
        return False
    def update_value(self, mouse_x):
        ratio = (mouse_x - self.rect.x) / self.rect.w
        ratio = max(0.0, min(1.0, ratio))
        self.value = self.min_val + (self.max_val - self.min_val) * ratio
        self.update_texture()
    def draw(self):
        glColor4f(0.3, 0.3, 0.3, 1.0)
        glBegin(GL_QUADS)
        glVertex2f(self.rect.x, self.rect.y + self.rect.h//2 - 2)
        glVertex2f(self.rect.x + self.rect.w, self.rect.y + self.rect.h//2 - 2)
        glVertex2f(self.rect.x + self.rect.w, self.rect.y + self.rect.h//2 + 2)
        glVertex2f(self.rect.x, self.rect.y + self.rect.h//2 + 2)
        glEnd()
        ratio = (self.value - self.min_val) / (self.max_val - self.min_val)
        kx = self.rect.x + ratio * self.rect.w - 5
        knob_color = (0.7, 0.7, 0.8, 1.0) if self.hovered or self.dragging else (0.5, 0.5, 0.6, 1.0)
        glColor4f(*knob_color)
        glBegin(GL_QUADS)
        glVertex2f(kx, self.rect.y); glVertex2f(kx + 10, self.rect.y)
        glVertex2f(kx + 10, self.rect.y + self.rect.h); glVertex2f(kx, self.rect.y + self.rect.h)
        glEnd()
        if hasattr(self, 'tex'):
            glEnable(GL_BLEND); glEnable(GL_TEXTURE_2D)
            glBindTexture(GL_TEXTURE_2D, self.tex)
            glColor4f(1, 1, 1, 1)
            tx = self.rect.x + (self.rect.w - self.tw) // 2
            ty = self.rect.y - self.th - 5 
            glBegin(GL_QUADS)
            glTexCoord2f(0, 0); glVertex2f(tx, ty + self.th)
            glTexCoord2f(1, 0); glVertex2f(tx + self.tw, ty + self.th)
            glTexCoord2f(1, 1); glVertex2f(tx + self.tw, ty)
            glTexCoord2f(0, 1); glVertex2f(tx, ty)
            glEnd()
            glDisable(GL_TEXTURE_2D); glDisable(GL_BLEND)
def normalize(v):
    norm = np.linalg.norm(v)
    if norm == 0: return v
    return v / norm
def ray_aabb_intersect(ray_origin, ray_dir, box_min, box_max):
    dir_fraction = np.empty(3, dtype=np.float32)
    dir_fraction[ray_dir == 0.0] = 1e30 
    dir_fraction[ray_dir != 0.0] = 1.0 / ray_dir[ray_dir != 0.0]
    t1 = (box_min - ray_origin) * dir_fraction
    t2 = (box_max - ray_origin) * dir_fraction
    t_min_v = np.minimum(t1, t2)
    t_max_v = np.maximum(t1, t2)
    t_enter = np.max(t_min_v)
    t_exit  = np.min(t_max_v)
    if t_exit < 0 or t_enter > t_exit:
        return None, None, None
    dist = t_enter if t_enter >= 0 else t_exit
    hit_point = ray_origin + ray_dir * dist
    center = (box_min + box_max) / 2.0
    size = (box_max - box_min)
    local_point = hit_point - center
    bias = local_point / (size * 0.5 + 1e-9)
    axis = np.argmax(np.abs(bias))
    sign = np.sign(bias[axis])
    normal = np.zeros(3)
    normal[axis] = sign
    return dist, hit_point, normal
def snap_value(val, precision=0.01):
    if precision == 0: return val
    return math.floor((val / precision) + 0.50001) * precision
def snap_vector(vec, precision=0.01):
    return np.array([
        snap_value(vec[0], precision),
        snap_value(vec[1], precision),
        snap_value(vec[2], precision)
    ], dtype=np.float32)
def snap_bounds_to_grid_3d(pos, scale, precision=0.01):
    pos = np.array(pos, dtype=np.float32)
    scale = np.array(scale, dtype=np.float32)
    half_scale = scale / 2.0
    p_min = pos - half_scale
    p_max = pos + half_scale
    def snap(val):
        return math.floor((val / precision) + 0.50001) * precision
    p_min_snapped = np.array([snap(p_min[0]), snap(p_min[1]), snap(p_min[2])], dtype=np.float32)
    p_max_snapped = np.array([snap(p_max[0]), snap(p_max[1]), snap(p_max[2])], dtype=np.float32)
    new_scale = p_max_snapped - p_min_snapped
    for i in range(3):
        if new_scale[i] < precision / 2:
            new_scale[i] = precision
            p_max_snapped[i] = p_min_snapped[i] + precision
    new_pos = p_min_snapped + new_scale / 2.0
    return new_pos, new_scale
class ColorPicker:
    def __init__(self, x, y, font):
        self.font = font
        self.active = False
        self.hsv = [0.0, 0.0, 1.0] 
        self.alpha = 1.0 
        self.emission = 0.0
        self.gloss = 0.0
        self.density = 1.0
        self.paint_all = False
        self.is_tiling_flag = False 
        self.current_texture_path = None
        self.base_width = 320
        self.base_height = 650
        self.scale = 1.0
        self.rect = pygame.Rect(x, y, self.base_width, self.base_height)
        self.history = []
        for i in range(30):
            val = 1.0 - (i / 30.0)
            self.history.append((val, val, val, 1.0, 0.0, 0.0, None, False, 1.0, 0.0))
        self.history_text_textures = []
        self._update_history_text_cache()
        self.spectrum_tex = self._generate_spectrum_texture()
        self.sliders = {
            'H': {'val': 0.0, 'col': (255,0,0), 'label': 'Hue', 'rect': pygame.Rect(0,0,0,0)},
            'S': {'val': 0.0, 'col': (0,255,0), 'label': 'Sat', 'rect': pygame.Rect(0,0,0,0)},
            'V': {'val': 1.0, 'col': (0,0,255), 'label': 'Val', 'rect': pygame.Rect(0,0,0,0)},
            'A': {'val': 1.0, 'col': (150,150,150), 'label': 'Alpha', 'rect': pygame.Rect(0,0,0,0)},
            'E': {'val': 0.0, 'col': (255,255,0), 'label': 'Emit', 'rect': pygame.Rect(0,0,0,0)},
            'G': {'val': 0.0, 'col': (200,200,255), 'label': 'Gloss', 'rect': pygame.Rect(0,0,0,0)},
            'D': {'val': 1.0, 'col': (100,255,255), 'label': 'Dens', 'rect': pygame.Rect(0,0,0,0)},
            'M': {'val': 0.0, 'col': (220,220,220), 'label': 'Mirr', 'rect': pygame.Rect(0,0,0,0)} 
        }
        self.reflectivity = 0.0 
        self.lbl_check_tex = safe_text_to_texture("Full", self.font, (220, 220, 220))
        self.lbl_tiling_tex = safe_text_to_texture("Tile", self.font, (220, 220, 220))
        self.lbl_h_tex = safe_text_to_texture("Hue", self.font, (200, 200, 200))
        self.lbl_s_tex = safe_text_to_texture("Sat", self.font, (200, 200, 200))
        self.lbl_v_tex = safe_text_to_texture("Val", self.font, (200, 200, 200))
        self.lbl_a_tex = safe_text_to_texture("Alpha", self.font, (200, 200, 200))
        self.lbl_e_tex = safe_text_to_texture("Emit", self.font, (200, 200, 200))
        self.lbl_g_tex = safe_text_to_texture("Gloss", self.font, (200, 200, 200))
        self.lbl_d_tex = safe_text_to_texture("Dens", self.font, (200, 200, 200)) 
        self.lbl_m_tex = safe_text_to_texture("Mirr", self.font, (200, 200, 200)) 
        self.lbl_tex_btn = safe_text_to_texture("Load Texture", self.font, (255, 255, 255))
        self.tex_btn_rect = pygame.Rect(0, 0, 0, 0)
        self.tex_val_str = None
        self.data_string = "255, 255, 255, 100, 0"
        self._update_string_texture()
        self.tex_name_val_tex = None 
        self.tex_name_str = "None"
        self.set_texture_name(None) 
        self.typing_rgb = False
        self.dragging_slider = None
        self.dragging_spectrum = False
        self.spectrum_rect = pygame.Rect(0,0,0,0)
        self.check_rect_area = pygame.Rect(0,0,0,0)
        self.check_tiling_rect = pygame.Rect(0,0,0,0)
        self.rgb_text_rect = pygame.Rect(0,0,0,0)
        self.history_rects = []
    def refresh_labels(self):
        # Импорт не нужен, если мы полагаемся на то, что TRANSLATIONS глобален
        # Но лучше брать язык из self.app (но у нас его нет в __init__)
        # Для простоты, допустим, мы пересоздадим текстуры на основе глобального словаря
        # Но мы не знаем текущий язык здесь.
        
        # Решение: App передаст текущий словарь переводов
        pass

    def update_language(self, tr_func):
        # tr_func - это self.app.tr
        
        # Удаляем старые текстуры
        for t in [self.lbl_check_tex, self.lbl_tiling_tex, self.lbl_h_tex, self.lbl_s_tex, 
                  self.lbl_v_tex, self.lbl_a_tex, self.lbl_e_tex, self.lbl_g_tex, 
                  self.lbl_d_tex, self.lbl_m_tex, self.lbl_tex_btn]:
            if t: glDeleteTextures([t[0]])

        # Создаем новые
        self.lbl_check_tex = safe_text_to_texture(tr_func('CP_FULL'), self.font, (220, 220, 220))
        self.lbl_tiling_tex = safe_text_to_texture(tr_func('CP_TILE'), self.font, (220, 220, 220))
        self.lbl_h_tex = safe_text_to_texture(tr_func('CP_HUE'), self.font, (200, 200, 200))
        self.lbl_s_tex = safe_text_to_texture(tr_func('CP_SAT'), self.font, (200, 200, 200))
        self.lbl_v_tex = safe_text_to_texture(tr_func('CP_VAL'), self.font, (200, 200, 200))
        self.lbl_a_tex = safe_text_to_texture(tr_func('CP_ALPHA'), self.font, (200, 200, 200))
        self.lbl_e_tex = safe_text_to_texture(tr_func('CP_EMIT'), self.font, (200, 200, 200))
        self.lbl_g_tex = safe_text_to_texture(tr_func('CP_GLOSS'), self.font, (200, 200, 200))
        self.lbl_d_tex = safe_text_to_texture(tr_func('CP_DENS'), self.font, (200, 200, 200)) 
        self.lbl_m_tex = safe_text_to_texture(tr_func('CP_MIRR'), self.font, (200, 200, 200)) 
        self.lbl_tex_btn = safe_text_to_texture(tr_func('CP_LOAD_TEX'), self.font, (255, 255, 255))
        
        # Обновляем динамические строки
        self.set_texture_name(self.current_texture_path, tr_func)
        self._update_string_texture(tr_func)
    def handle_event(self, event, on_texture_click=None):
        if not self.active: return False
        if event.type == sdl2.SDL_MOUSEWHEEL:
            return True
        if hasattr(event, 'pos'): mx, my = event.pos
        elif hasattr(event, 'motion'): mx, my = event.motion.x, event.motion.y
        elif hasattr(event, 'button'): mx, my = event.button.x, event.button.y
        else: mx, my = pygame.mouse.get_pos()
        if self.typing_rgb and event.type == sdl2.SDL_KEYDOWN:
            return False 
        if event.type == sdl2.SDL_MOUSEBUTTONDOWN:
            if event.button.button == sdl2.SDL_BUTTON_LEFT:
                if hasattr(self, 'tex_btn_rect') and self.tex_btn_rect.collidepoint(mx, my):
                    if on_texture_click:
                        on_texture_click()
                    return True
                if self.check_rect_area.inflate(10, 10).collidepoint(mx, my):
                    self.paint_all = not self.paint_all
                    return True
                if self.check_tiling_rect.inflate(10, 10).collidepoint(mx, my):
                    self.is_tiling_flag = not self.is_tiling_flag
                    return True
                if self.spectrum_rect.collidepoint(mx, my):
                    self.dragging_spectrum = True
                    self.update_spectrum(mx, my)
                    return True
                for key, sl in self.sliders.items():
                    touch_rect = sl['rect'].inflate(0, 15)
                    if touch_rect.collidepoint(mx, my):
                        self.dragging_slider = key
                        self.update_slider_val(key, mx)
                        return True
                if self.rgb_text_rect.collidepoint(mx, my):
                    self.typing_rgb = True
                else:
                    self.typing_rgb = False
                for i, r_rect in enumerate(self.history_rects):
                    if r_rect.collidepoint(mx, my):
                        val = self.history[i]
                        r, g, b = val[0], val[1], val[2]
                        a = val[3] if len(val) > 3 else 1.0
                        e = val[4] if len(val) > 4 else 0.0
                        gloss = val[5] if len(val) > 5 else 0.0 
                        tex_path = val[6] if len(val) > 6 else None
                        is_tiling = val[7] if len(val) > 7 else False
                        density = val[8] if len(val) > 8 else 1.0
                        self.set_full_data(r, g, b, a, e, gloss, tex_path, is_tiling, density)
                        return True
                if self.rect.collidepoint(mx, my):
                    return True
        elif event.type == sdl2.SDL_MOUSEBUTTONUP:
            self.dragging_slider = None
            self.dragging_spectrum = False
        elif event.type == sdl2.SDL_MOUSEMOTION:
            if self.dragging_slider:
                self.update_slider_val(self.dragging_slider, mx)
                return True
            if self.dragging_spectrum:
                self.update_spectrum(mx, my)
                return True
        return False
    def set_texture_name(self, name, tr_func=None):
        self.current_texture_path = name 
        if not name:
            txt = tr_func('CP_NO_TEX') if tr_func else "No Texture"
            self.tex_name_str = txt
            col = (150, 150, 150)
        else:
            self.tex_name_str = os.path.basename(name)
            if len(self.tex_name_str) > 25:
                self.tex_name_str = "..." + self.tex_name_str[-22:]
            col = (100, 255, 100)
        
        if self.tex_name_val_tex:
            glDeleteTextures([self.tex_name_val_tex[0]])
        prefix = tr_func('CP_FILE') if tr_func else "File"
        self.tex_name_val_tex = safe_text_to_texture(f"{prefix}: {self.tex_name_str}", self.font, col)
    def update_position(self, x, y, win_h):
        raw_scale = win_h / 700.0
        self.scale = max(1.2, min(1.8, raw_scale))
        curr_w = int(self.base_width * self.scale)
        curr_h = int(self.base_height * self.scale)
        self.rect = pygame.Rect(x, y, curr_w, curr_h)
        pad = int(10 * self.scale)
        inner_w = curr_w - 2 * pad
        spec_h = int(150 * self.scale)
        self.spectrum_rect = pygame.Rect(self.rect.x + pad, self.rect.y + pad, inner_w, spec_h)
        slider_h = int(15 * self.scale)
        slider_gap = int(15 * self.scale)
        start_y_sliders = self.spectrum_rect.bottom + pad
        order = ['H', 'S', 'V', 'A', 'E', 'G', 'D', 'M'] 
        for i, key in enumerate(order):
            sy = start_y_sliders + i * (slider_h + slider_gap)
            self.sliders[key]['rect'] = pygame.Rect(self.rect.x + pad, sy, inner_w, slider_h)
        last_slider_rect = self.sliders['M']['rect']
        text_field_h = int(30 * self.scale)
        text_field_y = last_slider_rect.bottom + pad
        self.rgb_text_rect = pygame.Rect(self.rect.x + pad, text_field_y, inner_w, text_field_h)
        hist_y_start = self.rgb_text_rect.bottom + pad
        chip_gap = int(5 * self.scale)
        chip_w = (inner_w - (5 * chip_gap)) // 6
        chip_h = int(15 * self.scale)
        self.history_rects = []
        for i in range(30):
            row = i // 6
            col = i % 6
            rx = self.rect.x + pad + col * (chip_w + chip_gap)
            ry = hist_y_start + row * (chip_h + chip_gap)
            self.history_rects.append(pygame.Rect(rx, ry, chip_w, chip_h))
        last_hist_rect = self.history_rects[-1]
        check_size = int(20 * self.scale)
        y_checks = last_hist_rect.bottom + pad * 2
        col_width = inner_w // 2 
        self.check_rect_area = pygame.Rect(self.rect.x + pad, y_checks, check_size, check_size)
        self.check_tiling_rect = pygame.Rect(self.rect.x + pad + col_width, y_checks, check_size, check_size)
        btn_h = int(30 * self.scale)
        btn_y = y_checks + check_size + pad * 2
        self.tex_btn_rect = pygame.Rect(self.rect.x + pad, btn_y, inner_w, btn_h)
    def _update_string_texture(self, tr_func=None):
        if self.tex_val_str:
            glDeleteTextures([self.tex_val_str[0]])
        prefix = tr_func('CP_DATA') if tr_func else "Data"
        self.tex_val_str = safe_text_to_texture(f"{prefix}: {self.data_string}", self.font, (255, 255, 255))
    def _generate_spectrum_texture(self):
        w, h = 300, 15
        surf = pygame.Surface((w, h))
        for x in range(w):
            hue = x / w
            rgb = colorsys.hsv_to_rgb(hue, 1.0, 1.0)
            col = (int(rgb[0]*255), int(rgb[1]*255), int(rgb[2]*255))
            pygame.draw.line(surf, col, (x, 0), (x, h))
        data = pygame.image.tostring(surf, "RGB", True)
        tex_id = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, tex_id)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, w, h, 0, GL_RGB, GL_UNSIGNED_BYTE, data)
        return tex_id
    def get_full_data(self):
        rgb = colorsys.hsv_to_rgb(self.hsv[0], self.hsv[1], self.hsv[2])
        return (rgb[0], rgb[1], rgb[2], self.alpha, self.emission, self.gloss, 
                self.current_texture_path, self.is_tiling_flag, self.density, self.reflectivity)
    def set_full_data(self, r, g, b, a, e, gloss=0.0, tex_path=None, is_tiling=False, density=1.0, reflectivity=0.0):
        self.hsv = list(colorsys.rgb_to_hsv(r, g, b))
        self.alpha = a
        self.emission = e
        self.gloss = gloss 
        self.is_tiling_flag = is_tiling
        self.density = density 
        self.reflectivity = reflectivity 
        self.set_texture_name(tex_path)
        self.update_ui_from_hsv()
    def _update_history_text_cache(self):
        if hasattr(self, 'history_text_textures'):
            for item in self.history_text_textures:
                if item:
                    try: glDeleteTextures([item[0]])
                    except: pass
        self.history_text_textures = []
        for val in self.history:
            tex_path = val[6] if len(val) > 6 else None
            if tex_path:
                name = os.path.basename(tex_path)
                short_name = name[:5]
                tex_data = safe_text_to_texture(short_name, self.font, (255, 255, 255))
                self.history_text_textures.append(tex_data)
            else:
                self.history_text_textures.append(None)
    def update_ui_from_hsv(self):
        self.sliders['H']['val'] = self.hsv[0]
        self.sliders['S']['val'] = self.hsv[1]
        self.sliders['V']['val'] = self.hsv[2]
        self.sliders['A']['val'] = self.alpha
        self.sliders['E']['val'] = self.emission
        self.sliders['G']['val'] = self.gloss
        self.sliders['D']['val'] = self.density
        self.sliders['M']['val'] = self.reflectivity 
        r, g, b, a, e, gloss, _, _, dens, refl = self.get_full_data()
        self.data_string = f"{int(r*255)}, {int(g*255)}, {int(b*255)}, {int(a*100)}, {int(e*100)}, {int(gloss*100)}, {int(dens*100)}, {int(refl*100)}"
        self._update_string_texture()
    def update_spectrum(self, mx, my):
        ratio_x = (mx - self.spectrum_rect.x) / self.spectrum_rect.w
        ratio_y = (my - self.spectrum_rect.y) / self.spectrum_rect.h
        self.hsv[0] = max(0.0, min(1.0, ratio_x))
        self.hsv[1] = 1.0 - max(0.0, min(1.0, ratio_y)) 
        self.update_ui_from_hsv()
    def update_slider_val(self, key, mx):
        sl = self.sliders[key]
        ratio = (mx - sl['rect'].x) / sl['rect'].w
        ratio = max(0.0, min(1.0, ratio))
        if key == 'H': self.hsv[0] = ratio
        elif key == 'S': self.hsv[1] = ratio
        elif key == 'V': self.hsv[2] = ratio
        elif key == 'A': self.alpha = ratio
        elif key == 'E': self.emission = ratio
        elif key == 'G': self.gloss = ratio
        elif key == 'D': self.density = ratio
        elif key == 'M': self.reflectivity = ratio 
        self.update_ui_from_hsv()
    def add_to_history(self):
        current = self.get_full_data()
        if not self.history or self.history[0] != current:
            self.history.insert(0, current)
            self.history.pop()
            self._update_history_text_cache()
    def draw_gl_texture(self, tex_data, x, y):
        tex_id, w, h = tex_data
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, tex_id)
        glColor4f(1, 1, 1, 1)
        glBegin(GL_QUADS)
        glTexCoord2f(0, 0); glVertex2f(x, y + h)
        glTexCoord2f(1, 0); glVertex2f(x + w, y + h)
        glTexCoord2f(1, 1); glVertex2f(x + w, y)
        glTexCoord2f(0, 1); glVertex2f(x, y)
        glEnd()
        glDisable(GL_TEXTURE_2D)
        glDisable(GL_BLEND)
    def draw(self):
        if not self.active: return
        glDisable(GL_TEXTURE_2D)
        glEnable(GL_BLEND)
        glColor4f(0.15, 0.15, 0.15, 0.95)
        glBegin(GL_QUADS)
        glVertex2f(self.rect.x, self.rect.y)
        glVertex2f(self.rect.x + self.rect.w, self.rect.y)
        glVertex2f(self.rect.x + self.rect.w, self.rect.y + self.rect.h)
        glVertex2f(self.rect.x, self.rect.y + self.rect.h)
        glEnd()
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, self.spectrum_tex)
        glColor3f(1,1,1)
        sx, sy, sw, sh = self.spectrum_rect
        glBegin(GL_QUADS)
        glTexCoord2f(0, 0); glVertex2f(sx, sy)
        glTexCoord2f(1, 0); glVertex2f(sx+sw, sy)
        glTexCoord2f(1, 1); glVertex2f(sx+sw, sy+sh)
        glTexCoord2f(0, 1); glVertex2f(sx, sy+sh)
        glEnd()
        glDisable(GL_TEXTURE_2D)
        cx = sx + self.hsv[0] * sw
        cy = sy + (1.0 - self.hsv[1]) * sh
        glColor3f(0,0,0); glLineWidth(2)
        cursor_sz = 5 * self.scale
        glBegin(GL_LINE_LOOP)
        glVertex2f(cx-cursor_sz, cy-cursor_sz); glVertex2f(cx+cursor_sz, cy-cursor_sz)
        glVertex2f(cx+cursor_sz, cy+cursor_sz); glVertex2f(cx-cursor_sz, cy+cursor_sz)
        glEnd()
        current_data = self.get_full_data()
        for key, sl in self.sliders.items():
            rx, ry, rw, rh = sl['rect']
            glBegin(GL_QUADS)
            if key == 'H': glColor3f(0.2, 0.2, 0.2) 
            else: glColor3f(0,0,0)
            glVertex2f(rx, ry); glVertex2f(rx, ry+rh)
            if key == 'H': glColor3f(0.5, 0.5, 0.5) 
            elif key == 'S': glColor3f(1,1,1) 
            elif key == 'V': glColor3f(current_data[0], current_data[1], current_data[2])
            elif key == 'A': glColor3f(0.8, 0.8, 0.8) 
            elif key == 'E': glColor3f(1.0, 1.0, 0.0)
            elif key == 'G': glColor3f(0.9, 0.9, 1.0) 
            elif key == 'D': glColor3f(0.4, 1.0, 1.0) 
            elif key == 'M': glColor3f(0.9, 0.9, 0.9) 
            glVertex2f(rx+rw, ry+rh); glVertex2f(rx+rw, ry)
            glEnd()
            if key == 'H':
                glEnable(GL_TEXTURE_2D)
                glBindTexture(GL_TEXTURE_2D, self.spectrum_tex)
                glColor3f(1,1,1)
                glBegin(GL_QUADS)
                glTexCoord2f(0, 0); glVertex2f(rx, ry)
                glTexCoord2f(1, 0); glVertex2f(rx+rw, ry)
                glTexCoord2f(1, 1); glVertex2f(rx+rw, ry+rh)
                glTexCoord2f(0, 1); glVertex2f(rx, ry+rh)
                glEnd()
                glDisable(GL_TEXTURE_2D)
            k_x = rx + sl['val'] * rw
            knob_w = 3 * self.scale
            knob_ext = 2 * self.scale
            glColor3f(0.8, 0.8, 0.8)
            glBegin(GL_QUADS)
            glVertex2f(k_x-knob_w, ry-knob_ext); glVertex2f(k_x+knob_w, ry-knob_ext)
            glVertex2f(k_x+knob_w, ry+rh+knob_ext); glVertex2f(k_x-knob_w, ry+rh+knob_ext)
            glEnd()
            tex = None
            if key == 'H': tex = self.lbl_h_tex
            elif key == 'S': tex = self.lbl_s_tex
            elif key == 'V': tex = self.lbl_v_tex
            elif key == 'A': tex = self.lbl_a_tex
            elif key == 'E': tex = self.lbl_e_tex
            elif key == 'G': tex = self.lbl_g_tex
            elif key == 'D': tex = self.lbl_d_tex
            elif key == 'M': tex = self.lbl_m_tex 
            if tex: self.draw_gl_texture(tex, rx + 5, ry - 2 * self.scale)
        glEnable(GL_BLEND) 
        for i, rect in enumerate(self.history_rects):
            val = self.history[i]
            r, g, b = val[0], val[1], val[2]
            a = val[3] if len(val) > 3 else 1.0
            glColor4f(r, g, b, a)
            glBegin(GL_QUADS)
            glVertex2f(rect.x, rect.y); glVertex2f(rect.right, rect.y)
            glVertex2f(rect.right, rect.bottom); glVertex2f(rect.x, rect.bottom)
            glEnd()
            if i < len(self.history_text_textures):
                tex_data = self.history_text_textures[i]
                if tex_data:
                    tex_id, tw, th = tex_data
                    tx = rect.x + (rect.w - tw) // 2
                    ty = rect.y + (rect.h - th) // 2
                    self.draw_gl_texture(tex_data, tx, ty)
        glDisable(GL_BLEND)
        glColor3f(0.2, 0.2, 0.2)
        rx, ry, rw, rh = self.rgb_text_rect
        if self.typing_rgb: glColor3f(0.3, 0.3, 0.5)
        glBegin(GL_QUADS)
        glVertex2f(rx, ry); glVertex2f(rx+rw, ry)
        glVertex2f(rx+rw, ry+rh); glVertex2f(rx, ry+rh)
        glEnd()
        if self.tex_val_str: self.draw_gl_texture(self.tex_val_str, rx + 5, ry + 5)
        cx, cy, cw, ch = self.check_rect_area
        glColor3f(1, 1, 1); glLineWidth(2)
        glBegin(GL_LINE_LOOP); glVertex2f(cx, cy); glVertex2f(cx+cw, cy); glVertex2f(cx+cw, cy+ch); glVertex2f(cx, cy+ch); glEnd()
        if self.paint_all:
            inset = 4 * self.scale; glColor3f(0, 1, 0)
            glBegin(GL_QUADS); glVertex2f(cx+inset, cy+inset); glVertex2f(cx+cw-inset, cy+inset); glVertex2f(cx+cw-inset, cy+ch-inset); glVertex2f(cx+inset, cy+ch-inset); glEnd()
        self.draw_gl_texture(self.lbl_check_tex, cx + cw + 5, cy)
        cx, cy, cw, ch = self.check_tiling_rect
        glColor3f(1, 1, 1); glLineWidth(2)
        glBegin(GL_LINE_LOOP); glVertex2f(cx, cy); glVertex2f(cx+cw, cy); glVertex2f(cx+cw, cy+ch); glVertex2f(cx, cy+ch); glEnd()
        if self.is_tiling_flag:
            inset = 4 * self.scale; glColor3f(0, 1, 0)
            glBegin(GL_QUADS); glVertex2f(cx+inset, cy+inset); glVertex2f(cx+cw-inset, cy+inset); glVertex2f(cx+cw-inset, cy+ch-inset); glVertex2f(cx+inset, cy+ch-inset); glEnd()
        self.draw_gl_texture(self.lbl_tiling_tex, cx + cw + 5, cy)
        tx, ty, tw, th = self.tex_btn_rect
        col = (0.3, 0.3, 0.3)
        mx, my = pygame.mouse.get_pos()
        if self.tex_btn_rect.collidepoint(mx, my): col = (0.4, 0.4, 0.4)
        glColor3f(*col)
        glBegin(GL_QUADS)
        glVertex2f(tx, ty); glVertex2f(tx+tw, ty)
        glVertex2f(tx+tw, ty+th); glVertex2f(tx, ty+th)
        glEnd()
        if self.lbl_tex_btn:
            tex_id, l_w, l_h = self.lbl_tex_btn
            draw_x = tx + (tw - l_w) // 2
            draw_y = ty + (th - l_h) // 2
            self.draw_gl_texture(self.lbl_tex_btn, draw_x, draw_y)
        if self.tex_name_val_tex:
            tx = self.rect.x + 10 * self.scale
            ty = self.tex_btn_rect.bottom + 10 * self.scale
            self.draw_gl_texture(self.tex_name_val_tex, tx, ty)
class FileDialog:
    def __init__(self, font):
        self.tr_func = lambda x: x # По умолчанию возвращает ключ
        self.font = font
        self.active = False
        self.mode = 'save'
        self.current_path = os.getcwd()
        self.history = [self.current_path]
        self.history_index = 0
        self.file_list = [] 
        self.list_textures = [] 
        self.sidebar_items = []
        self.sidebar_textures = []
        self.scroll_offset = 0
        self.selected_index = -1
        self.filename_input = "save.ant"
        self.edit_cursor = 0 
        self.callback = None
        self.input_focused = False
        self.path_input = ""
        self.path_cursor = 0
        self.path_focused = False
        self.selection_anchor = None
        self.held_key = None
        self.held_mod = None
        self.repeat_timer = 0
        self.initial_repeat_delay = 400
        self.repeat_interval = 40
        self.undo_stack = []
        self.redo_stack = []
        self.view_mode = 'list'
        self.sort_by = 'name'
        self.sort_reverse = False
        self.win_w = 800
        self.win_h = 600
        self.rect = pygame.Rect(0, 0, 100, 100)
        self.sidebar_width = 160
        self.top_panel_height = 40
        self.footer_height = 60
        self.header_height = 30
        self.item_height_list = 25
        self.item_width_grid = 100
        self.item_height_grid = 110
        self.col_size_w = 90
        self.col_date_w = 140
        self.icon_size = 15
        self.max_visible_items = 10
        self.cols_in_grid = 1
        self.text_offset_x = 30
        self.lbl_path_tex = None
        self.path_w = 0
        self.path_h = 0
        self.export_formats = ['GLB', 'OBJ', 'STL']
        self.current_fmt_idx = 0
        self.is_exporting = False
        self.is_render = False
    def update_layout(self, w, h, font):
        self.win_w = w
        self.win_h = h
        self.font = font 
        fh = self.font.get_height()
        self.item_height_list = int(fh * 1.5)
        self.header_height = int(fh * 1.6)
        self.top_panel_height = int(fh * 2.2)
        self.footer_height = int(fh * 3.0)
        self.icon_size = int(fh)
        self.text_offset_x = 5 + self.icon_size + 10
        self.item_width_grid = int(fh * 6.0)
        self.item_height_grid = int(fh * 6.5)
        self.col_date_w = int(fh * 9.0)
        self.col_size_w = int(fh * 5.0)
        target_w = max(640, int(w * 0.75))
        target_h = max(480, int(h * 0.75))
        self.sidebar_width = max(120, int(fh * 10)) 
        x = (w - target_w) // 2
        y = (h - target_h) // 2
        self.rect = pygame.Rect(x, y, target_w, target_h)
        self.recalc_visible_area()
        if self.active:
            self.cleanup()
            self.regenerate_sidebar()
            self.refresh_items()
    def recalc_visible_area(self):
        list_h = self.rect.h - self.top_panel_height - self.header_height - self.footer_height
        if self.view_mode == 'grid':
            list_h += self.header_height
        list_w = self.rect.w - self.sidebar_width
        if self.view_mode == 'list':
            self.max_visible_items = max(1, list_h // self.item_height_list)
        else:
            self.cols_in_grid = max(1, list_w // self.item_width_grid)
            rows = max(1, list_h // self.item_height_grid)
            self.max_visible_items = rows * self.cols_in_grid
    def get_active_field_info(self):
        if self.path_focused: return self.path_input, self.path_cursor, self.selection_anchor
        elif self.input_focused: return self.filename_input, self.edit_cursor, self.selection_anchor
        return None, 0, None
    def set_active_field_info(self, text, cursor, anchor):
        if self.path_focused: self.path_input = text; self.path_cursor = cursor; self.selection_anchor = anchor
        elif self.input_focused: self.filename_input = text; self.edit_cursor = cursor; self.selection_anchor = anchor
    def get_char_index_at_x(self, text, local_x):
        if local_x <= 0: return 0
        best_idx = 0
        min_dist = float('inf')
        for i in range(len(text) + 1):
            sub = text[:i]
            w = self.font.size(sub)[0]
            dist = abs(w - local_x)
            if dist < min_dist: min_dist = dist; best_idx = i
            else: break
        return best_idx
    def refresh_ui_text(self, tr_func=None):
        # Метод просто должен существовать, чтобы App мог его вызвать.
        # Поскольку FileDialog перерисовывается каждый кадр (или при refresh_items), 
        # нам нужно внедрить tr_func в сам класс.
        if tr_func:
            self.tr_func = tr_func
            self.refresh_items() # Пересоздаст текстуры списка
            self.regenerate_sidebar() # Пересоздаст сайдбар

    def update(self):
        if not self.active: return
        if self.held_key is not None:
            now = pygame.time.get_ticks()
            if now >= self.repeat_timer:
                self.process_key_action(self.held_key, self.held_mod)
                self.repeat_timer = now + self.repeat_interval
    def process_key_action(self, key, mod):
        text, cursor, anchor = self.get_active_field_info()
        if text is None: return
        def remove_selection(t, c, a):
            if a is None: return t, c
            start, end = sorted((c, a))
            return t[:start] + t[end:], start
        def save_snapshot():
            if len(self.undo_stack) > 50: self.undo_stack.pop(0)
            self.undo_stack.append((text, cursor))
            self.redo_stack.clear()
        if key == sdl2.SDLK_z and (mod & sdl2.KMOD_CTRL):
            if self.undo_stack:
                self.redo_stack.append((text, cursor))
                prev_text, prev_cursor = self.undo_stack.pop()
                self.set_active_field_info(prev_text, prev_cursor, None)
            return
        elif key == sdl2.SDLK_y and (mod & sdl2.KMOD_CTRL):
            if self.redo_stack:
                self.undo_stack.append((text, cursor))
                next_text, next_cursor = self.redo_stack.pop()
                self.set_active_field_info(next_text, next_cursor, None)
            return
        if key == sdl2.SDLK_LEFT:
            if mod & sdl2.KMOD_SHIFT:
                if anchor is None: anchor = cursor
                cursor = max(0, cursor - 1)
            else:
                if anchor is not None: cursor = min(cursor, anchor); anchor = None
                else: cursor = max(0, cursor - 1)
        elif key == sdl2.SDLK_RIGHT:
            if mod & sdl2.KMOD_SHIFT:
                if anchor is None: anchor = cursor
                cursor = min(len(text), cursor + 1)
            else:
                if anchor is not None: cursor = max(cursor, anchor); anchor = None
                else: cursor = min(len(text), cursor + 1)
        elif key == sdl2.SDLK_HOME:
            if mod & sdl2.KMOD_SHIFT:
                if anchor is None: anchor = cursor
                cursor = 0
            else: cursor = 0; anchor = None
        elif key == sdl2.SDLK_END:
            if mod & sdl2.KMOD_SHIFT:
                if anchor is None: anchor = cursor
                cursor = len(text)
            else: cursor = len(text); anchor = None
        elif key == sdl2.SDLK_a and (mod & sdl2.KMOD_CTRL):
            anchor = 0; cursor = len(text)
        elif key == sdl2.SDLK_c and (mod & sdl2.KMOD_CTRL):
            if anchor is not None and anchor != cursor:
                start, end = sorted((cursor, anchor))
                try: sdl2.SDL_SetClipboardText(text[start:end].encode('utf-8'))
                except: pass
        elif key == sdl2.SDLK_v and (mod & sdl2.KMOD_CTRL):
            try:
                clipboard = sdl2.SDL_GetClipboardText()
                if clipboard:
                    save_snapshot()
                    if anchor is not None:
                        text, cursor = remove_selection(text, cursor, anchor)
                        anchor = None
                    paste_text = clipboard.decode('utf-8')
                    text = text[:cursor] + paste_text + text[cursor:]
                    cursor += len(paste_text)
            except: pass
        elif key == sdl2.SDLK_BACKSPACE:
            if len(text) > 0 or anchor is not None:
                save_snapshot()
                if anchor is not None:
                    text, cursor = remove_selection(text, cursor, anchor)
                    anchor = None
                elif cursor > 0:
                    text = text[:cursor-1] + text[cursor:]
                    cursor -= 1
        elif key == sdl2.SDLK_DELETE:
            if len(text) > 0 or anchor is not None:
                save_snapshot()
                if anchor is not None:
                    text, cursor = remove_selection(text, cursor, anchor)
                    anchor = None
                elif cursor < len(text):
                    text = text[:cursor] + text[cursor+1:]
        self.set_active_field_info(text, cursor, anchor)
    def process_text_input(self, input_text):
        text, cursor, anchor = self.get_active_field_info()
        if text is None: return
        if len(self.undo_stack) > 50: self.undo_stack.pop(0)
        self.undo_stack.append((text, cursor))
        self.redo_stack.clear()
        if anchor is not None:
            start, end = sorted((cursor, anchor))
            text = text[:start] + text[end:]
            cursor = start
            anchor = None
        text = text[:cursor] + input_text + text[cursor:]
        cursor += len(input_text)
        self.set_active_field_info(text, cursor, anchor)
    def cleanup(self):
        for row in self.list_textures:
            for item in row:
                if item and item[0]: 
                    try: glDeleteTextures([item[0]])
                    except: pass
        self.list_textures = []
        for tex, _, _ in self.sidebar_textures:
            if tex: 
                try: glDeleteTextures([tex])
                except: pass
        self.sidebar_textures = []
        if self.lbl_path_tex: 
            try: glDeleteTextures([self.lbl_path_tex])
            except: pass
            self.lbl_path_tex = None
        glBindTexture(GL_TEXTURE_2D, 0)
    def regenerate_sidebar(self):
        for tex, _, _ in self.sidebar_textures:
            if tex: 
                try: glDeleteTextures([tex])
                except: pass
        self.sidebar_textures = []
        self.sidebar_items = self.get_system_paths()
        for name_key, _, is_special in self.sidebar_items:
            # Переводим ключ, если это диск (C:\) он не найдется в словаре и вернется как есть
            disp_name = self.tr_func(name_key) 
            color = (100, 200, 255) if is_special else (200, 200, 200)
            tex, w, h = safe_text_to_texture(f" {disp_name}", self.font, color)
            self.sidebar_textures.append((tex, w, h))
        glBindTexture(GL_TEXTURE_2D, 0)
    def format_size(self, size):
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024: return f"{size:.1f} {unit}"
            size /= 1024
        return f"{size:.1f} TB"
    def refresh_items(self):
        for row in self.list_textures:
            for item in row:
                if item and item[0]: 
                    try: glDeleteTextures([item[0]])
                    except: pass
        self.list_textures = []
        if self.lbl_path_tex: 
            try: glDeleteTextures([self.lbl_path_tex])
            except: pass
            self.lbl_path_tex = None
        self.file_list = []
        self.selected_index = -1
        self.scroll_offset = 0
        try:
            with os.scandir(self.current_path) as it:
                for entry in it:
                    if self.is_hidden(entry.path): continue
                    is_dir = entry.is_dir()
                    if not is_dir:
                        if self.extensions:
                            if not any(entry.name.lower().endswith(ext) for ext in self.extensions):
                                continue
                        else:
                            if not (entry.name.endswith(".ant") or entry.name.endswith(".zip") or entry.name.endswith(".json")): 
                                continue
                    try:
                        stat = entry.stat()
                        size = stat.st_size if not is_dir else 0
                        mtime = stat.st_mtime
                    except: size = 0; mtime = 0
                    self.file_list.append({'name': entry.name, 'is_dir': is_dir, 'size': size, 'date': mtime})
        except: pass
        def sort_key(item):
            val = item[self.sort_by]
            if self.sort_by == 'name': return val.lower()
            return val
        self.file_list.sort(key=sort_key, reverse=self.sort_reverse)
        self.file_list = [f for f in self.file_list if f['is_dir']] + [f for f in self.file_list if not f['is_dir']]
        for item in self.file_list:
            name = item['name']
            if self.view_mode == 'list':
                list_w = self.rect.w - self.sidebar_width - self.col_size_w - self.col_date_w - self.text_offset_x - 20
                char_w = max(5, self.font.size("A")[0])
                max_chars = max(8, list_w // char_w)
                disp_name = name if len(name) < max_chars else name[:max_chars-3] + "..."
            else:
                disp_name = name if len(name) < 13 else name[:10] + "..."
            tex_n, w_n, h_n = safe_text_to_texture(disp_name, self.font, (255, 255, 255))
            tex_d, w_d, h_d = None, 0, 0
            tex_s, w_s, h_s = None, 0, 0
            if self.view_mode == 'list':
                date_str = datetime.datetime.fromtimestamp(item['date']).strftime("%Y-%m-%d %H:%M")
                tex_d, w_d, h_d = safe_text_to_texture(date_str, self.font, (255, 255, 255))
                size_str = "" if item['is_dir'] else self.format_size(item['size'])
                if size_str:
                    tex_s, w_s, h_s = safe_text_to_texture(size_str, self.font, (255, 255, 255))
            self.list_textures.append([(tex_n, w_n, h_n), (tex_d, w_d, h_d), (tex_s, w_s, h_s)])
        p_str = self.current_path
        if not self.path_focused:
            max_chars = int((self.rect.w - 150) / self.font.size("A")[0])
            if len(p_str) > max_chars: p_str = "..." + p_str[-(max_chars-3):]
            self.lbl_path_tex, self.path_w, self.path_h = safe_text_to_texture(p_str, self.font, (255, 255, 255))
        glBindTexture(GL_TEXTURE_2D, 0)
    def get_system_paths(self):
        paths = []
        home = os.path.expanduser("~")
        # Используем ключи словаря
        paths.append(("FD_DESKTOP", os.path.join(home, "Desktop"), True))
        paths.append(("FD_DOCS", os.path.join(home, "Documents"), True))
        paths.append(("FD_DOWN", os.path.join(home, "Downloads"), True))
        drives = []
        if sys.platform == 'win32':
            bitmask = ctypes.windll.kernel32.GetLogicalDrives()
            for letter in string.ascii_uppercase:
                if bitmask & 1: drives.append(f"{letter}:\\")
                bitmask >>= 1
        else:
            drives.append("/")
        for d in drives: paths.append((d, d, False))
        return paths
    def is_hidden(self, filepath):
        if sys.platform == 'win32':
            try:
                attrs = ctypes.windll.kernel32.GetFileAttributesW(filepath)
                if attrs != -1 and (attrs & 2): return True
            except: pass
        return os.path.basename(filepath).startswith('.') or '$' in filepath
    def change_path(self, new_path, add_to_history=True):
        try:
            os.scandir(new_path).close()
            self.current_path = new_path
            if add_to_history:
                if self.history_index < len(self.history) - 1:
                    self.history = self.history[:self.history_index+1]
                self.history.append(new_path)
                self.history_index = len(self.history) - 1
            self.refresh_items()
        except Exception as e:
            print(f"Access Error: {e}")
    def go_back(self):
        if self.history_index > 0:
            self.history_index -= 1
            self.change_path(self.history[self.history_index], add_to_history=False)
    def go_forward(self):
        if self.history_index < len(self.history) - 1:
            self.history_index += 1
            self.change_path(self.history[self.history_index], add_to_history=False)
    def go_up(self):
        parent = os.path.dirname(self.current_path)
        if parent and parent != self.current_path:
            self.change_path(parent)
    def toggle_view(self):
        self.view_mode = 'grid' if self.view_mode == 'list' else 'list'
        self.recalc_visible_area()
        self.scroll_offset = 0
        self.refresh_items()
    def open(self, mode, callback, extensions=None, is_export=False, is_render=False):
        self.active = True
        self.mode = mode
        self.callback = callback
        self.extensions = extensions
        self.is_exporting = is_export
        self.is_render = is_render # Запоминаем режим рендера
        
        if mode == 'load':
            self.filename_input = ""
        elif mode == 'save':
            if self.is_exporting:
                # Ставим расширение по умолчанию для экспорта 3D
                ext = self.export_formats[self.current_format_idx].split()[0].lower()
                self.filename_input = f"export.{ext}"
            elif self.is_render:
                # Имя для видео
                self.filename_input = "cinematic.mp4"
                self.render_loop = False
            else:
                self.filename_input = "new_file.ant"
        
        self.edit_cursor = len(self.filename_input)
        self.input_focused = True
        self.path_focused = False
        self.undo_stack = []
        self.redo_stack = []
        self.cleanup()
        self.regenerate_sidebar()
        self.refresh_items()
    def close(self):
        self.active = False
        if self.callback: self.callback(None)
        self.callback = None
        self.held_key = None
        self.cleanup()
    def handle_event(self, event):
        if not self.active: return False
        if event.type == sdl2.SDL_MOUSEWHEEL:
            mx, my = pygame.mouse.get_pos()
            if self.rect.collidepoint(mx, my):
                list_area_y = self.rect.y + self.top_panel_height
                if self.view_mode == 'list': list_area_y += self.header_height
                if my > list_area_y and my < self.rect.bottom - self.footer_height and mx > self.rect.x + self.sidebar_width:
                    self.scroll_offset -= event.wheel.y
                    if self.view_mode == 'list':
                         max_scroll = max(0, len(self.file_list) - self.max_visible_items)
                    else:
                        total_rows = (len(self.file_list) + self.cols_in_grid - 1) // self.cols_in_grid
                        visible_rows = self.max_visible_items // self.cols_in_grid
                        max_scroll = max(0, total_rows - visible_rows) * self.cols_in_grid
                    self.scroll_offset = max(0, min(self.scroll_offset, max_scroll))
            return True
        if event.type == sdl2.SDL_MOUSEBUTTONDOWN:
            mx, my = event.button.x, event.button.y
            if not self.rect.collidepoint(mx, my): return True 
            bh = int(self.font.get_height() * 1.5)
            btn_y = self.rect.y + (self.top_panel_height - bh) // 2
            bx = self.rect.x + 10
            path_start = bx+(bh+5)*3 + 10
            vw = self.font.size("View")[0] + 20
            path_end = self.rect.right - vw - 20
            path_rect = pygame.Rect(path_start, btn_y, path_end - path_start, bh)
            if path_rect.collidepoint(mx, my):
                if not self.path_focused:
                    self.path_focused = True
                    self.input_focused = False
                    self.path_input = self.current_path
                    self.path_cursor = len(self.path_input)
                    self.held_key = None
                    self.undo_stack = []
                    self.redo_stack = []
                    if self.lbl_path_tex: 
                        try: glDeleteTextures([self.lbl_path_tex])
                        except: pass
                        self.lbl_path_tex = None
                local_x = mx - (path_rect.x + 5)
                self.path_cursor = self.get_char_index_at_x(self.path_input, local_x)
                self.selection_anchor = None
                return True 
            else:
                if self.path_focused:
                    self.path_focused = False
                    self.refresh_items()
            if my < self.rect.y + self.top_panel_height:
                if pygame.Rect(bx, btn_y, bh, bh).collidepoint(mx, my): self.go_back(); return True
                if pygame.Rect(bx+bh+5, btn_y, bh, bh).collidepoint(mx, my): self.go_forward(); return True
                if pygame.Rect(bx+(bh+5)*2, btn_y, bh, bh).collidepoint(mx, my): self.go_up(); return True
                if pygame.Rect(self.rect.right - vw - 10, btn_y, vw, bh).collidepoint(mx, my): self.toggle_view(); return True
            sb_y = self.rect.y + self.top_panel_height
            if mx < self.rect.x + self.sidebar_width and my > sb_y and my < self.rect.bottom - self.footer_height:
                idx = (my - sb_y) // self.item_height_list
                if 0 <= idx < len(self.sidebar_items): self.change_path(self.sidebar_items[idx][1])
                return True
            list_start_y = sb_y
            if self.view_mode == 'list': list_start_y += self.header_height
            list_rect = pygame.Rect(self.rect.x + self.sidebar_width, list_start_y, 
                                    self.rect.w - self.sidebar_width, 
                                    self.rect.bottom - self.footer_height - list_start_y)
            if self.view_mode == 'list' and sb_y <= my < list_start_y:
                area_w = self.rect.w - self.sidebar_width
                rel_x = mx - (self.rect.x + self.sidebar_width)
                x_size = area_w - self.col_size_w
                x_date = x_size - self.col_date_w
                new_sort = 'name'
                if rel_x > x_size: new_sort = 'size'
                elif rel_x > x_date: new_sort = 'date'
                if self.sort_by == new_sort: self.sort_reverse = not self.sort_reverse
                else: self.sort_by = new_sort; self.sort_reverse = False
                self.refresh_items(); return True
            if list_rect.collidepoint(mx, my):
                self.input_focused = False
                self.selection_anchor = None
                rel_y = my - list_start_y
                rel_x = mx - list_rect.x
                idx = -1
                if self.view_mode == 'list':
                    idx = self.scroll_offset + int(rel_y // self.item_height_list)
                else:
                    col = int(rel_x // self.item_width_grid)
                    row = int(rel_y // self.item_height_grid)
                    start_idx = (self.scroll_offset // self.cols_in_grid) * self.cols_in_grid
                    idx = start_idx + row * self.cols_in_grid + col
                if 0 <= idx < len(self.file_list):
                    if self.selected_index == idx and event.button.clicks == 2:
                        self.enter_item(idx)
                    else:
                        self.selected_index = idx
                        item = self.file_list[idx]
                        if not item['is_dir']: 
                            self.filename_input = item['name']
                            self.edit_cursor = len(self.filename_input)
                            self.input_focused = True
                            self.undo_stack = []
                            self.redo_stack = []
                return True
            foot_y = self.rect.bottom - self.footer_height
            inp_h = int(self.footer_height * 0.6)
            inp_x = self.rect.x + self.sidebar_width // 2
            inp_w = self.rect.w - self.sidebar_width - 180
            inp_rect = pygame.Rect(inp_x, foot_y + (self.footer_height-inp_h)//2, inp_w, inp_h)
            if inp_rect.collidepoint(mx, my):
                if not self.input_focused:
                    self.undo_stack = [] 
                    self.redo_stack = []
                self.input_focused = True
                self.path_focused = False 
                self.refresh_items()
                local_x = mx - (inp_rect.x + 5)
                self.edit_cursor = self.get_char_index_at_x(self.filename_input, local_x)
                self.selection_anchor = None
            else:
                pass
            btn_h = int(self.font.get_height() * 1.5)
            btn_w = 80
            btn_y_foot = foot_y + (self.footer_height - btn_h) // 2
            if self.mode == 'save' and self.is_exporting:
                fmt_str = f"{self.tr_func('FD_FMT')}: {self.export_formats[self.current_fmt_idx]}"
                fmt_btn_w = int(self.font.size(fmt_str)[0] + 20)
                fmt_x = self.rect.right - 200 - fmt_btn_w - 10
                if pygame.Rect(fmt_x, btn_y_foot, fmt_btn_w, btn_h).collidepoint(mx, my):
                    self.current_fmt_idx = (self.current_fmt_idx + 1) % len(self.export_formats)
                    new_ext = self.export_formats[self.current_fmt_idx].lower()
                    base = os.path.splitext(self.filename_input)[0]
                    self.filename_input = f"{base}.{new_ext}"
                    return True
        
            if pygame.Rect(self.rect.right - 20 - btn_w, btn_y_foot, btn_w, btn_h).collidepoint(mx, my): self.confirm(); return True
            if pygame.Rect(self.rect.right - 30 - btn_w*2, btn_y_foot, btn_w, btn_h).collidepoint(mx, my): self.close(); return True
            return True
        if event.type == sdl2.SDL_KEYDOWN:
            key = event.key.keysym.sym
            mod = event.key.keysym.mod
            if key == sdl2.SDLK_ESCAPE: 
                if self.path_focused:
                    self.path_focused = False
                    self.selection_anchor = None
                    self.refresh_items()
                else:
                    self.close()
            elif key == sdl2.SDLK_RETURN: 
                if self.path_focused:
                    if os.path.isdir(self.path_input):
                        self.change_path(self.path_input)
                        self.path_focused = False
                        self.input_focused = True
                    else:
                        print("Invalid path")
                else:
                    self.confirm()
            elif self.input_focused or self.path_focused:
                self.held_key = key
                self.held_mod = mod
                self.repeat_timer = pygame.time.get_ticks() + self.initial_repeat_delay
                self.process_key_action(key, mod)
            return True
        if event.type == sdl2.SDL_KEYUP:
            if event.key.keysym.sym == self.held_key:
                self.held_key = None
            return True
        return False
    def enter_item(self, idx):
        item = self.file_list[idx]
        if item['is_dir']:
            self.change_path(os.path.join(self.current_path, item['name']))
        else:
            self.filename_input = item['name']
            self.confirm()
    def confirm(self):
        if not self.filename_input: return
        full = os.path.join(self.current_path, self.filename_input)
        
        # --- ИСПРАВЛЕНИЕ: Логика расширений ---
        if self.mode == 'save':
            if self.is_render:
                # Рендер видео: Только .mp4
                # Убираем .ant если он случайно там оказался
                if full.endswith('.ant'): full = full[:-4]
                if not full.endswith('.mp4'): full += ".mp4"
                
            elif self.is_exporting:
                # Экспорт 3D
                current_ext = "." + self.export_formats[self.current_fmt_idx].lower()
                # Если расширение не совпадает ни с одним из допустимых
                if not any(full.lower().endswith(fmt.lower()) for fmt in ['.glb', '.obj', '.stl']):
                    full += current_ext
            elif self.is_render:
                # Рендер видео: Только .mp4
                # Очищаем от мусора в конце, если он есть
                if full.endswith('.ant'): full = full[:-4]
                # Простая проверка: если нет .mp4 на конце, добавляем
                if not full.lower().endswith('.mp4'): 
                    full += ".mp4"
            else:
                # Обычное сохранение проекта
                if not (full.endswith('.ant') or full.endswith('.zip') or full.endswith('.json')): 
                    full += ".ant"
        # --------------------------------------
        if self.mode == 'load' and not os.path.isfile(full): return
        if self.callback: self.callback(full)
        self.active = False
        self.callback = None
        self.cleanup()
    def draw_rect(self, x, y, w, h, color):
        glColor4f(*color)
        glBegin(GL_QUADS)
        glVertex2f(x, y); glVertex2f(x + w, y)
        glVertex2f(x + w, y + h); glVertex2f(x, y + h)
        glEnd()
    def draw_gl_texture(self, tex_id, x, y, w, h):
        if not tex_id: return
        glEnable(GL_TEXTURE_2D); glBindTexture(GL_TEXTURE_2D, tex_id)
        glBegin(GL_QUADS)
        glTexCoord2f(0, 0); glVertex2f(x, y + h)
        glTexCoord2f(1, 0); glVertex2f(x + w, y + h)
        glTexCoord2f(1, 1); glVertex2f(x + w, y)
        glTexCoord2f(0, 1); glVertex2f(x, y)
        glEnd(); glDisable(GL_TEXTURE_2D)
    def draw_icon(self, x, y, is_dir, w, h):
        if is_dir:
            glColor4f(0.9, 0.7, 0.2, 1.0)
            glBegin(GL_QUADS)
            glVertex2f(x, y + h*0.2); glVertex2f(x+w, y + h*0.2)
            glVertex2f(x+w, y+h); glVertex2f(x, y+h)
            glEnd()
            glBegin(GL_QUADS)
            glVertex2f(x, y); glVertex2f(x+w*0.4, y)
            glVertex2f(x+w*0.4, y+h*0.2); glVertex2f(x, y+h*0.2)
            glEnd()
        else:
            glColor4f(0.9, 0.9, 0.9, 1.0)
            glBegin(GL_QUADS)
            glVertex2f(x+w*0.2, y); glVertex2f(x+w*0.8, y)
            glVertex2f(x+w*0.8, y+h); glVertex2f(x+w*0.2, y+h)
            glEnd()
            glColor4f(0.5, 0.5, 0.5, 1.0); glLineWidth(1)
            glBegin(GL_LINES)
            for i in range(1, 4):
                yy = y + h * (0.3 + i*0.15)
                glVertex2f(x+w*0.3, yy); glVertex2f(x+w*0.7, yy)
            glEnd()
    def draw(self):
        if not self.active: return
        glEnable(GL_BLEND); glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        self.draw_rect(0, 0, self.win_w, self.win_h, (0, 0, 0, 0.6))
        self.draw_rect(self.rect.x, self.rect.y, self.rect.w, self.rect.h, (0.2, 0.2, 0.2, 1.0))
        self.draw_rect(self.rect.x, self.rect.y, self.rect.w, self.top_panel_height, (0.25, 0.25, 0.25, 1.0))
        bh = int(self.font.get_height() * 1.5)
        btn_y = self.rect.y + (self.top_panel_height - bh) // 2
        bx = self.rect.x + 10
        def btn(lbl, x, w, h):
            self.draw_rect(x, btn_y, w, h, (0.4,0.4,0.4,1))
            t, tw, th = safe_text_to_texture(lbl, self.font, (255,255,255))
            if t:
                glColor4f(1,1,1,1)
                self.draw_gl_texture(t, x+(w-tw)//2, btn_y+(h-th)//2, tw, th)
                glDeleteTextures([t])
        btn("<", bx, bh, bh)
        btn(">", bx+bh+5, bh, bh)
        btn("^", bx+(bh+5)*2, bh, bh)
        path_start = bx+(bh+5)*3 + 10
        vw = self.font.size("View")[0] + 20
        path_end = self.rect.right - vw - 20
        path_w = path_end - path_start
        path_h = bh
        self.draw_rect(path_start, btn_y, path_w, path_h, (0.1,0.1,0.1,1) if self.path_focused else (0.15,0.15,0.15,1))
        if self.path_focused:
            glLineWidth(2); glColor4f(0,0.5,1,1)
            glBegin(GL_LINE_LOOP)
            glVertex2f(path_start, btn_y); glVertex2f(path_start+path_w, btn_y)
            glVertex2f(path_start+path_w, btn_y+path_h); glVertex2f(path_start, btn_y+path_h)
            glEnd()
            draw_y = btn_y + (path_h - self.font.get_height()) // 2
            draw_x = path_start + 5
            if self.selection_anchor is not None and self.selection_anchor != self.path_cursor:
                start, end = sorted((self.path_cursor, self.selection_anchor))
                pre_w = self.font.size(self.path_input[:start])[0]
                sel_w = self.font.size(self.path_input[start:end])[0]
                self.draw_rect(draw_x + pre_w, draw_y, sel_w, self.font.get_height(), (0.0, 0.4, 0.8, 0.6))
            pt, pw, ph = safe_text_to_texture(self.path_input, self.font, (255,255,255))
            if pt:
                if pw > path_w - 10: draw_x = path_start + path_w - pw - 5
                glColor4f(1,1,1,1)
                self.draw_gl_texture(pt, draw_x, draw_y, pw, ph)
                glDeleteTextures([pt])
                if (pygame.time.get_ticks() // 500) % 2 == 0:
                    sub = self.path_input[:self.path_cursor]
                    cw = self.font.size(sub)[0]
                    cur_x = draw_x + cw + 2
                    if cur_x < path_start + path_w - 2 and cur_x > path_start:
                        glLineWidth(1); glColor4f(1,1,1,1)
                        glBegin(GL_LINES); glVertex2f(cur_x, draw_y); glVertex2f(cur_x, draw_y+ph); glEnd()
        else:
            if self.lbl_path_tex:
                draw_y = btn_y + (path_h - self.path_h) // 2
                glColor4f(1,1,1,1)
                self.draw_gl_texture(self.lbl_path_tex, path_start+5, draw_y, self.path_w, self.path_h)
        btn(self.tr_func('FD_VIEW'), self.rect.right - vw - 10, vw, bh)
        sb_y = self.rect.y + self.top_panel_height
        sb_h = self.rect.h - self.top_panel_height - self.footer_height
        self.draw_rect(self.rect.x, sb_y, self.sidebar_width, sb_h, (0.15,0.15,0.15,1))
        norm_cur = os.path.normpath(self.current_path)
        for i, (tex, w, h) in enumerate(self.sidebar_textures):
            item_y = sb_y + 5 + i * self.item_height_list
            if i < len(self.sidebar_items):
                item_path = self.sidebar_items[i][1]
                norm_item = os.path.normpath(item_path)
                is_selected = False
                try:
                    if sys.platform == 'win32': nc, ni = norm_cur.lower(), norm_item.lower()
                    else: nc, ni = norm_cur, norm_item
                    if nc == ni or nc.startswith(ni + os.sep): is_selected = True
                except: pass
                if is_selected:
                    self.draw_rect(self.rect.x, item_y, self.sidebar_width, self.item_height_list, (0.3, 0.4, 0.5, 1.0))
            text_y = item_y + (self.item_height_list - h) // 2
            glColor4f(1,1,1,1)
            self.draw_gl_texture(tex, self.rect.x+10, text_y, w, h)
        area_x = self.rect.x + self.sidebar_width
        area_w = self.rect.w - self.sidebar_width
        start_y = sb_y
        if self.view_mode == 'list':
            self.draw_rect(area_x, sb_y, area_w, self.header_height, (0.3,0.3,0.3,1))
            x_size = area_x + area_w - self.col_size_w
            x_date = x_size - self.col_date_w
            header_map = {self.tr_func('FD_NAME'): 'name', self.tr_func('FD_DATE'): 'date', self.tr_func('FD_SIZE'): 'size'}
            def hdr(txt, x):
                t, w, h = safe_text_to_texture(txt, self.font, (255,255,255))
                if t:
                    y = sb_y + (self.header_height - h) // 2
                    glColor4f(1,1,1,1)
                    self.draw_gl_texture(t, x, y, w, h)
                    sort_key = header_map.get(txt)
                    if sort_key == self.sort_by:
                        tri_x = x + w + 8
                        tri_y = y + h/2
                        tri_sz = 4
                        glColor4f(1, 1, 0, 1) 
                        glBegin(GL_TRIANGLES)
                        if self.sort_reverse: 
                            glVertex2f(tri_x - tri_sz, tri_y - tri_sz/2)
                            glVertex2f(tri_x + tri_sz, tri_y - tri_sz/2)
                            glVertex2f(tri_x, tri_y + tri_sz)
                        else: 
                            glVertex2f(tri_x, tri_y - tri_sz)
                            glVertex2f(tri_x - tri_sz, tri_y + tri_sz/2)
                            glVertex2f(tri_x + tri_sz, tri_y + tri_sz/2)
                        glEnd()
                    glDeleteTextures([t])
            hdr(self.tr_func('FD_NAME'), area_x + 10)
            hdr(self.tr_func('FD_DATE'), x_date + 5)
            hdr(self.tr_func('FD_SIZE'), x_size + 5)
            start_y += self.header_height
        if self.view_mode == 'list':
            item_x_size = area_x + area_w - self.col_size_w
            item_x_date = item_x_size - self.col_date_w
            for i in range(self.max_visible_items):
                idx = self.scroll_offset + i
                if idx >= len(self.file_list): break
                iy = start_y + i * self.item_height_list
                if idx == self.selected_index: 
                    self.draw_rect(area_x, iy, area_w, self.item_height_list, (0,0.4,0.8,0.8))
                item = self.file_list[idx]
                texs = self.list_textures[idx]
                icon_y = iy + (self.item_height_list - self.icon_size) // 2
                self.draw_icon(area_x+5, icon_y, item['is_dir'], self.icon_size, self.icon_size)
                text_y = iy + (self.item_height_list - texs[0][2]) // 2 
                glColor4f(1,1,1,1)
                if texs[0][0]: self.draw_gl_texture(texs[0][0], area_x + self.text_offset_x, text_y, texs[0][1], texs[0][2])
                if texs[1][0]: self.draw_gl_texture(texs[1][0], item_x_date+5, text_y, texs[1][1], texs[1][2])
                if texs[2][0]: self.draw_gl_texture(texs[2][0], item_x_size+5, text_y, texs[2][1], texs[2][2])
        else:
            start_idx = (self.scroll_offset // self.cols_in_grid) * self.cols_in_grid
            for i in range(self.max_visible_items):
                idx = start_idx + i
                if idx >= len(self.file_list): break
                row = i // self.cols_in_grid
                col = i % self.cols_in_grid
                ix = area_x + col * self.item_width_grid
                iy = start_y + row * self.item_height_grid
                if iy + self.item_height_grid > start_y + sb_h: break
                if idx == self.selected_index:
                    self.draw_rect(ix+5, iy+5, self.item_width_grid-10, self.item_height_grid-10, (0,0.4,0.8,0.5))
                item = self.file_list[idx]
                icon_dim = int(self.item_width_grid * 0.5)
                icon_x = ix + (self.item_width_grid - icon_dim) // 2
                self.draw_icon(icon_x, iy+10, item['is_dir'], icon_dim, icon_dim)
                tex_n = self.list_textures[idx][0]
                if tex_n[0]:
                    tx = ix + (self.item_width_grid - tex_n[1]) // 2
                    ty = iy + 10 + icon_dim + 10
                    glColor4f(1,1,1,1)
                    self.draw_gl_texture(tex_n[0], tx, ty, tex_n[1], tex_n[2])
        fy = self.rect.bottom - self.footer_height
        self.draw_rect(self.rect.x, fy, self.rect.w, self.footer_height, (0.25,0.25,0.25,1))
        inp_h = int(self.footer_height * 0.6)
        inp_x = self.rect.x + self.sidebar_width // 2
        inp_w = self.rect.w - self.sidebar_width - 180
        self.draw_rect(inp_x, fy + (self.footer_height-inp_h)//2, inp_w, inp_h, (0.1,0.1,0.1,1))
        if self.input_focused:
            glLineWidth(2); glColor4f(0,0.5,1,1)
            glBegin(GL_LINE_LOOP)
            glVertex2f(inp_x, fy+(self.footer_height-inp_h)//2); glVertex2f(inp_x+inp_w, fy+(self.footer_height-inp_h)//2)
            glVertex2f(inp_x+inp_w, fy+(self.footer_height+inp_h)//2); glVertex2f(inp_x, fy+(self.footer_height+inp_h)//2)
            glEnd()
        draw_x = inp_x + 5
        draw_y = fy + (self.footer_height - self.font.get_height()) // 2
        if self.input_focused and self.selection_anchor is not None and self.selection_anchor != self.edit_cursor:
            start, end = sorted((self.edit_cursor, self.selection_anchor))
            pre_w = self.font.size(self.filename_input[:start])[0]
            sel_w = self.font.size(self.filename_input[start:end])[0]
            self.draw_rect(draw_x + pre_w, draw_y, sel_w, self.font.get_height(), (0.0, 0.4, 0.8, 0.6))
        it, iw, ih = safe_text_to_texture(self.filename_input, self.font, (255,255,255))
        if it:
            glColor4f(1,1,1,1)
            self.draw_gl_texture(it, draw_x, draw_y, iw, ih)
            glDeleteTextures([it])
        if self.input_focused and (pygame.time.get_ticks() // 500) % 2 == 0:
            sub_str = self.filename_input[:self.edit_cursor]
            cw = self.font.size(sub_str)[0]
            cx = draw_x + cw + 2
            glLineWidth(1); glColor4f(1,1,1,1)
            glBegin(GL_LINES); glVertex2f(cx, draw_y); glVertex2f(cx, draw_y+ih); glEnd()
        btn_h = int(self.font.get_height() * 1.5)
        btn_y = fy + (self.footer_height - btn_h) // 2
        def fbtn(l, x):
            self.draw_rect(x, btn_y, 80, btn_h, (0.4,0.4,0.4,1))
            t, w, h = safe_text_to_texture(l, self.font, (255,255,255))
            if t:
                glColor4f(1,1,1,1)
                self.draw_gl_texture(t, x+(80-w)//2, btn_y+(btn_h-h)//2, w, h)
                glDeleteTextures([t])
        if self.mode == 'save' and self.is_exporting:
            fmt_str = f"{self.tr_func('FD_FMT')}: {self.export_formats[self.current_fmt_idx]}"
            fmt_w = int(self.font.size(fmt_str)[0] + 20)
            fmt_x = self.rect.right - 190 - fmt_w - 10 
            self.draw_rect(fmt_x, btn_y, fmt_w, btn_h, (0.2, 0.5, 0.6, 1.0))
            t_fmt, w_fmt, h_fmt = safe_text_to_texture(fmt_str, self.font, (255, 255, 255))
            if t_fmt:
                glColor4f(1,1,1,1)
                self.draw_gl_texture(t_fmt, fmt_x + (fmt_w-w_fmt)//2, btn_y+(btn_h-h_fmt)//2, w_fmt, h_fmt)
                glDeleteTextures([t_fmt])
        
        # --- ЗДЕСЬ БЫЛ КОД RENDER LOOP UI, ОН ТЕПЕРЬ УДАЛЕН ---

        fbtn(self.tr_func('FD_CANCEL'), self.rect.right-190)
        fbtn(self.tr_func('FD_OK'), self.rect.right-100)
        glDisable(GL_BLEND)
class Camera:
    def __init__(self):
        self.pos = np.array([0.0, 1.8, 5.0], dtype=np.float32)
        self.visual_y = self.pos[1] 
        self.yaw = -90.0
        self.pitch = 0.0
        self.speed = 5.0
        self.mouse_sensitivity = 0.1
        self.update_vectors()
    def update_vectors(self):
        front = np.array([
            math.cos(math.radians(self.yaw)) * math.cos(math.radians(self.pitch)),
            math.sin(math.radians(self.pitch)),
            math.sin(math.radians(self.yaw)) * math.cos(math.radians(self.pitch))
        ])
        self.front = normalize(front)
        self.right = normalize(np.cross(self.front, np.array([0, 1, 0])))
        self.up = normalize(np.cross(self.right, self.front))
    def process_mouse(self, dx, dy):
        self.yaw += dx * self.mouse_sensitivity
        self.pitch -= dy * self.mouse_sensitivity
        self.pitch = max(-89.0, min(89.0, self.pitch))
        self.update_vectors()
    def move(self, keys, dt):
        velocity = self.speed * dt
        if keys.get(sdl2.SDLK_LSHIFT): self.pos -= np.array([0, 1, 0]) * velocity
        if keys.get(sdl2.SDLK_SPACE): self.pos += np.array([0, 1, 0]) * velocity
        flat_front = np.array([self.front[0], 0, self.front[2]])
        flat_front = normalize(flat_front)
        flat_right = self.right
        if keys.get(sdl2.SDLK_w): self.pos += flat_front * velocity
        if keys.get(sdl2.SDLK_s): self.pos -= flat_front * velocity
        if keys.get(sdl2.SDLK_a): self.pos -= flat_right * velocity
        if keys.get(sdl2.SDLK_d): self.pos += flat_right * velocity
        self.visual_y = self.pos[1]
    def update_smooth_y(self, dt, speed=6.0):
        # speed=6.0 дает примерно 0.6 секунды на завершение движения
        diff = self.pos[1] - self.visual_y
        
        # Если разница огромная (например, телепорт или респаун), перемещаем мгновенно
        if abs(diff) > 20.0:
            self.visual_y = self.pos[1]
        else:
            # Экспоненциальное сглаживание (Lerp)
            # visual_y стремится к pos[1]
            self.visual_y += diff * speed * dt
def lerp(start, end, factor):
    return start + (end - start) * factor
class CloudRenderer:
    def __init__(self, tex_id):
        self.tex_id = tex_id
        
        # Настройки текстуры (Мипмаппинг оставляем, он полезен)
        glBindTexture(GL_TEXTURE_2D, self.tex_id)
        glGenerateMipmap(GL_TEXTURE_2D) 
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glBindTexture(GL_TEXTURE_2D, 0)

        self.vao = glGenVertexArrays(1)
        self.vbo = glGenBuffers(1) 
        self.ebo = glGenBuffers(1)
        
        self.smooth_vis = 0.0
        self.smooth_color = np.array([1.0, 1.0, 1.0], dtype=np.float32)

        self.shader = Shader("""
            #version 330 core
            layout (location = 0) in vec3 aPos;
            layout (location = 1) in vec2 aTex;
            uniform mat4 view;
            uniform mat4 projection;
            uniform mat4 model;
            uniform vec2 uvOffset;
            uniform float cloudScale;
            out vec2 vTex;
            out vec3 FragPos; 
            void main() {
                vec4 worldPos = model * vec4(aPos, 1.0);
                gl_Position = projection * view * worldPos;
                FragPos = vec3(worldPos);
                // Базовые координаты
                vTex = aTex * cloudScale + uvOffset; 
            }
        """, """
            #version 330 core
            out vec4 FragColor;
            in vec2 vTex;
            in vec3 FragPos;
            
            uniform sampler2D cloudTex;
            uniform vec4 cloudColorTint;
            uniform float visibility;
            uniform vec3 viewPos;
            uniform float fogLimit; 

            // Функция поворота UV координат
            vec2 rotate(vec2 uv, float angle) {
                float s = sin(angle);
                float c = cos(angle);
                mat2 rot = mat2(c, -s, s, c);
                return rot * uv;
            }

            void main() {
                // === 1. СЛОИ ОБЛАКОВ (FBM) ===
                
                // Слой 1: Базовая форма (крупные детали)
                vec4 col1 = texture(cloudTex, vTex);
                
                // Слой 2: Детали (мелкие, повернутые)
                // Сдвигаем координаты, масштабируем (1.6x) и поворачиваем (~30 градусов)
                // Это полностью ломает сетку повторений.
                vec2 uv2 = vTex * 1.6 + vec2(2.3, 5.1); 
                uv2 = rotate(uv2, 0.5); 
                vec4 col2 = texture(cloudTex, uv2);

                // Смешиваем слои. 
                // Базовый слой важнее (0.6), детали добавляют шум (0.4)
                float combinedAlpha = col1.a * 0.6 + col2.a * 0.4;
                
                // === 2. ФОРМИРОВАНИЕ ОБЪЕМА (Soft Threshold) ===
                // Здесь мы отсекаем "мусор" и делаем облака более очерченными.
                // low (0.4) - всё что ниже этого, станет прозрачным (убирает дымку на фоне)
                // high (0.8) - где плотность высокая, там будет полное облако
                float density = smoothstep(0.2, 0.6, combinedAlpha);

                // Если плотность 0, не рисуем (оптимизация)
                if (density < 0.01) discard;

                // === 3. ЦВЕТ И ТУМАН ===
                vec3 finalRGB = cloudColorTint.rgb;
                
                // Итоговая прозрачность
                float alpha = density * visibility;

                // Радиальный туман (мягкое исчезновение вдалеке)
                float dist = length(FragPos - viewPos);
                float fadeStart = fogLimit * 0.6;
                float fadeEnd = fogLimit * 0.95;
                float fogFactor = (fadeEnd - dist) / (fadeEnd - fadeStart);
                fogFactor = clamp(fogFactor, 0.0, 1.0);
                
                alpha *= fogFactor;
                
                FragColor = vec4(finalRGB, alpha);
            }
        """)

        # Геометрия (стандартная плоскость)
        vertices = np.array([
            -0.5, 0.0, -0.5,  0.0, 0.0,
             0.5, 0.0, -0.5,  1.0, 0.0,
             0.5, 0.0,  0.5,  1.0, 1.0,
            -0.5, 0.0,  0.5,  0.0, 1.0,
        ], dtype=np.float32)
        indices = np.array([0, 1, 2, 2, 3, 0], dtype=np.uint32)

        glBindVertexArray(self.vao)
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.ebo)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices.nbytes, indices, GL_STATIC_DRAW)
        
        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 5 * 4, ctypes.c_void_p(0))
        glEnableVertexAttribArray(1)
        glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, 5 * 4, ctypes.c_void_p(12))
        glBindVertexArray(0)

        self.cloud_offset_x = 0.0
        self.cloud_offset_z = 0.0

    def update(self, dt, sun_speed=0.25):
        # ... (Код update без изменений) ...
        wind_speed = sun_speed * 0.004 
        self.cloud_offset_x += wind_speed * dt
        self.cloud_offset_z += (wind_speed * 0.6) * dt 

    def draw(self, view, proj, cam_pos, light_color, light_intensity, dt, fog_dist):
        # ... (Код draw без изменений, используем self.smooth_vis как раньше) ...
        self.shader.use()
        glDisable(GL_CULL_FACE)
        
        cloud_height = 100.0 
        plane_size = max(fog_dist * 10.0, 6000.0)
        
        # Матрицы
        m_trans = MatrixUtils.translation(cam_pos[0], cloud_height, cam_pos[2])
        m_scale = MatrixUtils.scale(plane_size, 1.0, plane_size)
        model = m_trans @ m_scale
        
        self.shader.set_mat4("view", view)
        self.shader.set_mat4("projection", proj)
        self.shader.set_mat4("model", model)
        glUniform3f(glGetUniformLocation(self.shader.program, "viewPos"), *cam_pos)
        
        limit = min(fog_dist * 6.0, plane_size * 0.48)
        glUniform1f(glGetUniformLocation(self.shader.program, "fogLimit"), limit)

        # Текстурные сдвиги
        world_scale_factor = 6000.0 
        tiling = plane_size / world_scale_factor
        u_shift = self.cloud_offset_x + (cam_pos[0] / plane_size) * tiling
        v_shift = self.cloud_offset_z + (cam_pos[2] / plane_size) * tiling
        glUniform2f(glGetUniformLocation(self.shader.program, "uvOffset"), u_shift, v_shift)
        glUniform1f(glGetUniformLocation(self.shader.program, "cloudScale"), tiling)

        # Плавный цвет
        target_tint = np.array(light_color) * 0.8 + 0.2
        color_lerp = min(2.0 * dt, 1.0)
        self.smooth_color = lerp(self.smooth_color, target_tint, color_lerp)
        glUniform4f(glGetUniformLocation(self.shader.program, "cloudColorTint"), *self.smooth_color, 1.0)

        # Плавная видимость
        target_vis = 0.15 + (light_intensity * 0.85)
        vis_lerp = min(1.5 * dt, 1.0)
        self.smooth_vis = lerp(self.smooth_vis, target_vis, vis_lerp)
        glUniform1f(glGetUniformLocation(self.shader.program, "visibility"), self.smooth_vis)

        # Рендер
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, self.tex_id)
        glUniform1i(glGetUniformLocation(self.shader.program, "cloudTex"), 0)
        
        glDepthMask(False)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        
        glBindVertexArray(self.vao)
        glDrawElements(GL_TRIANGLES, 6, GL_UNSIGNED_INT, None)
        glBindVertexArray(0)
        
        glDepthMask(True)
        glDisable(GL_BLEND)
        glEnable(GL_CULL_FACE)
class Entity:
    __slots__ = [
        'uid', 'pos', 'scale', 'group_id', 'group_history', 
        'faces_colors', 'faces_textures', 'faces_uv_data',
        'faces_tiling', 
        'brightness', 'is_door', 'door_open',
        'hinge_edge', 'is_animating', 'is_hole', 'door_angle',
        'density', 'faces_reflectivity'  
    ]
    def __init__(self, pos, scale, group_id=None, color=None, group_history=None, faces_colors=None, faces_textures=None, faces_uv_data=None):
        self.uid = uuid.uuid4().hex
        self.group_id = group_id
        self.group_history = group_history if group_history is not None else []
        clean_pos, clean_scale = snap_bounds_to_grid_3d(pos, scale, precision=0.01)
        self.pos = clean_pos
        self.scale = clean_scale
        base_color = color if color else (1.0, 1.0, 1.0)
        if faces_colors:
            self.faces_colors = faces_colors
        else:
            self.faces_colors = [base_color] * 6
        if faces_textures:
            self.faces_textures = faces_textures
        else:
            self.faces_textures = [None] * 6
        if faces_uv_data: 
            self.faces_uv_data = faces_uv_data
        else:
            self.faces_uv_data = [{'off': [0.0, 0.0], 'scl': [1.0, 1.0], 'rot': 0, 'fliph': 0, 'flipv': 0} for _ in range(6)]
        self.brightness = 1.0
        self.is_door = False
        self.door_open = False
        self.hinge_edge = -1 
        self.is_animating = False
        self.is_hole = False
        self.door_angle = 0.0
        self.faces_tiling = [False] * 6 
        self.density = 1.0
        self.faces_reflectivity = [0.0] * 6
    def get_aabb(self):
        half = self.scale / 2.0
        return self.pos - half, self.pos + half
    def to_dict(self):
        return {
            "uid": self.uid,
            "type": "wall",
            "group_id": self.group_id,
            "group_history": self.group_history,
            "is_door": self.is_door,
            "door_open": self.door_open, 
            "hinge_edge": self.hinge_edge,
            "is_hole": self.is_hole,
            "faces_tiling": self.faces_tiling,
            "faces_reflectivity": self.faces_reflectivity,
            "density": self.density,
            "position": self.pos.tolist(),
            "scale": self.scale.tolist(),
            "faces_colors": self.faces_colors,
            "faces_textures": self.faces_textures,
            "faces_uv_data": self.faces_uv_data 
        }
    @staticmethod
    def from_dict(data):
        color = data.get('color')
        faces = data.get('faces_colors')
        textures = data.get('faces_textures', [None]*6)
        uv_data = data.get('faces_uv_data')
        if not uv_data:
            uv_data = [{'off': [0.0, 0.0], 'scl': [1.0, 1.0], 'rot': 0, 'fliph': 0, 'flipv': 0} for _ in range(6)]
        ent = Entity(
            data['position'], 
            data['scale'], 
            data.get('group_id'), 
            color,
            data.get('group_history'),
            faces,
            textures,
            uv_data
        )
        ent.uid = data['uid']
        ent.is_door = data.get('is_door', False)
        ent.door_open = data.get('door_open', False)
        ent.is_hole = data.get('is_hole', False)
        ent.hinge_edge = data.get('hinge_edge', -1)
        ent.is_animating = False
        if 'faces_tiling' in data:
            ent.faces_tiling = data['faces_tiling']
        else:
            old_val = data.get('is_tiling', False)
            ent.faces_tiling = [old_val] * 6
        if 'density' in data:
            ent.density = data['density']
        else:
            if data.get('is_ghost', False):
                ent.density = 0.0
            else:
                ent.density = 1.0
        if 'faces_reflectivity' in data:
            ent.faces_reflectivity = data['faces_reflectivity']
        else:
            ent.faces_reflectivity = [0.0] * 6
        return ent
    def update_from_dict(self, data):
        self.pos = np.array(data['position'], dtype=np.float32)
        self.scale = np.array(data['scale'], dtype=np.float32)
        self.group_id = data.get('group_id')
        self.group_history = data.get('group_history', [])
        self.is_door = data.get('is_door', False)
        self.door_open = data.get('door_open', False)
        self.hinge_edge = data.get('hinge_edge', -1)
        self.is_hole = data.get('is_hole', False)
        if 'density' in data:
            self.density = data['density']
        elif 'is_ghost' in data:
            self.density = 0.0 if data['is_ghost'] else 1.0
        if 'faces_colors' in data:
            self.faces_colors = copy.deepcopy(data['faces_colors'])
        if 'faces_textures' in data:
            self.faces_textures = copy.deepcopy(data['faces_textures'])
        if 'faces_uv_data' in data:
            self.faces_uv_data = copy.deepcopy(data['faces_uv_data'])
        if 'faces_tiling' in data:
            self.faces_tiling = copy.deepcopy(data['faces_tiling'])
        elif 'is_tiling' in data:
            old_val = data['is_tiling']
            self.faces_tiling = [old_val] * 6
        if 'faces_reflectivity' in data:
            self.faces_reflectivity = copy.deepcopy(data['faces_reflectivity'])
        else:
            self.faces_reflectivity = [0.0] * 6
class Scene:
    def __init__(self):
        self.entities = []
        self.undo_stack = []
        self.redo_stack = []
        self.max_history = 100
    def add_entity(self, ent, record_undo=True):
        self.entities.append(ent)
        if record_undo:
            entry = {'added': [ent.to_dict()], 'removed': [], 'modified': []}
            self._push_to_history(entry)
    def remove_entity(self, ent, record_undo=True):
        if ent in self.entities:
            self.entities.remove(ent)
            if record_undo:
                entry = {'added': [], 'removed': [ent.to_dict()], 'modified': []}
                self._push_to_history(entry)
    def merge_last_modification(self, after_states):
        if not self.undo_stack: return False
        last_entry = self.undo_stack[-1]
        if last_entry.get('added') or last_entry.get('removed'): return False
        if not last_entry.get('modified'): return False
        last_uids = set(t[0] for t in last_entry['modified'])
        current_uids = set(after_states.keys())
        if last_uids != current_uids: return False
        new_modified_list = []
        for uid, state_before, _old_state_after in last_entry['modified']:
            new_modified_list.append((uid, state_before, after_states[uid]))
        last_entry['modified'] = new_modified_list
        return True
    def undo(self):
        if not self.undo_stack: return []
        action = self.undo_stack.pop()
        self.redo_stack.append(action)
        affected_entities = []
        for data in action['added']:
            ent = self.get_entity_by_uid(data['uid'])
            if ent:
                affected_entities.append(ent)
                self.entities.remove(ent)
        for data in action['removed']:
            new_ent = Entity.from_dict(data)
            self.entities.append(new_ent)
            affected_entities.append(new_ent)
        for uid, state_before, state_after in action['modified']:
            ent = self.get_entity_by_uid(uid)
            if ent:
                affected_entities.append(ent)
                ent.update_from_dict(state_before)
        return affected_entities
    def redo(self):
        if not self.redo_stack: return []
        action = self.redo_stack.pop()
        self.undo_stack.append(action)
        affected_entities = []
        for data in action['added']:
            new_ent = Entity.from_dict(data)
            self.entities.append(new_ent)
            affected_entities.append(new_ent)
        for data in action['removed']:
            ent = self.get_entity_by_uid(data['uid'])
            if ent:
                affected_entities.append(ent)
                self.entities.remove(ent)
        for uid, state_before, state_after in action['modified']:
            ent = self.get_entity_by_uid(uid)
            if ent:
                affected_entities.append(ent)
                ent.update_from_dict(state_after)
        return affected_entities
    def clear(self):
        self.entities = []
        self.undo_stack = []
        self.redo_stack = []
    def raycast(self, ray_origin, ray_dir, ignore_holes=False, candidates=None):
        closest_dist = np.inf
        closest_ent = None
        closest_norm = None
        iterator = candidates if candidates is not None else self.entities
        for ent in iterator:
            if ignore_holes and ent.is_hole:
                continue
            b_min, b_max = ent.get_aabb()
            if ent.is_hole:
                height = b_max[1] - b_min[1]
                if height < 0.5: 
                    center_y = (b_min[1] + b_max[1]) / 2.0
                    b_min[1] = center_y - 0.25
                    b_max[1] = center_y + 0.25
            dist, point, norm = ray_aabb_intersect(ray_origin, ray_dir, b_min, b_max)
            if dist is not None and dist < closest_dist:
                closest_dist = dist
                closest_ent = ent
                closest_norm = norm
        return closest_ent, closest_dist, closest_norm
    def get_entity_by_uid(self, uid):
        for ent in self.entities:
            if ent.uid == uid: return ent
        return None
    def push_modification(self, before_states, after_states):
        mod_list = []
        for uid in before_states:
            if uid in after_states:
                if before_states[uid] != after_states[uid]:
                    mod_list.append((uid, before_states[uid], after_states[uid]))
        if mod_list:
            entry = {'added': [], 'removed': [], 'modified': mod_list}
            self._push_to_history(entry)
    def push_transaction(self, added_ents, removed_ents, modified_triplets):
        entry = {
            'added': [e.to_dict() for e in added_ents],
            'removed': [e.to_dict() for e in removed_ents],
            'modified': []
        }
        for ent, old_d, new_d in modified_triplets:
            entry['modified'].append((ent.uid, old_d, new_d))
        self._push_to_history(entry)
    def _push_to_history(self, entry):
        if entry['added'] or entry['removed'] or entry['modified']:
            self.undo_stack.append(entry)
            self.redo_stack.clear() 
            if len(self.undo_stack) > self.max_history:
                self.undo_stack.pop(0)
class DynamicFloorRenderer:
    def __init__(self):
        self.mesh = None
        self.last_cx = None
        self.last_cz = None
        self.last_radius = None
        self.CHUNK_SIZE = 10.0
    def update(self, center_cx, center_cz, radius_chunks):
        if (self.last_cx == center_cx and 
            self.last_cz == center_cz and 
            self.last_radius == radius_chunks):
            return
        self.last_cx = center_cx
        self.last_cz = center_cz
        self.last_radius = radius_chunks
        if self.mesh:
            self.mesh.delete()
            self.mesh = None
        buffer_data = []
        gr, gg, gb = COLOR_GROUND
        ga = 1.0; gem = 0.0; gloss = 0.0
        reflect = 0.0 
        nx, ny, nz = 0.0, 1.0, 0.0
        uv_scale = UV_SCALE
        r2 = radius_chunks * radius_chunks
        for dx in range(-radius_chunks, radius_chunks + 1):
            for dz in range(-radius_chunks, radius_chunks + 1):
                if dx*dx + dz*dz > r2:
                    continue
                cx = center_cx + dx
                cz = center_cz + dz
                x0 = cx * self.CHUNK_SIZE
                z0 = cz * self.CHUNK_SIZE
                x1 = x0 + self.CHUNK_SIZE
                z1 = z0 + self.CHUNK_SIZE
                y = 0.0
                u0, v0 = x0 * uv_scale, z0 * uv_scale
                u1, v1 = x1 * uv_scale, z1 * uv_scale
                p1 = [x0, y, z1, gr, gg, gb, ga, nx, ny, nz, u0, v1, gem, gloss, reflect]
                p2 = [x1, y, z1, gr, gg, gb, ga, nx, ny, nz, u1, v1, gem, gloss, reflect]
                p3 = [x1, y, z0, gr, gg, gb, ga, nx, ny, nz, u1, v0, gem, gloss, reflect]
                p4 = [x0, y, z0, gr, gg, gb, ga, nx, ny, nz, u0, v0, gem, gloss, reflect]
                buffer_data.extend(p1 + p2 + p3)
                buffer_data.extend(p1 + p3 + p4)
        if buffer_data:
            arr = np.array(buffer_data, dtype=np.float32)
            self.mesh = MeshBuffer(arr)
    def draw(self):
        if self.mesh:
            self.mesh.draw()
class StarRenderer:
    def __init__(self, count=6210): 
        self.count = count
        self.vao = glGenVertexArrays(1)
        self.vbo = glGenBuffers(1)
        data = []
        for _ in range(count):
            phi = np.random.uniform(0, 2 * math.pi)
            costheta = np.random.uniform(-1, 1)
            theta = math.acos(costheta)
            x = math.sin(theta) * math.cos(phi)
            y = math.sin(theta) * math.sin(phi)
            z = math.cos(theta)
            rand_val = np.random.random()
            if rand_val > 0.98:
                size = np.random.uniform(2.5, 4.0) 
            elif rand_val > 0.7:
                size = np.random.uniform(1.5, 2.5) 
            else:
                size = np.random.uniform(0.8, 1.5) 
            data.extend([x, y, z, size])
        buffer_np = np.array(data, dtype=np.float32)
        glBindVertexArray(self.vao)
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        glBufferData(GL_ARRAY_BUFFER, buffer_np.nbytes, buffer_np, GL_STATIC_DRAW)
        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 4 * 4, ctypes.c_void_p(0))
        glEnableVertexAttribArray(1)
        glVertexAttribPointer(1, 1, GL_FLOAT, GL_FALSE, 4 * 4, ctypes.c_void_p(12))
        glBindVertexArray(0)
        self.shader = Shader("""
            #version 330 core
            layout (location = 0) in vec3 aPos;
            layout (location = 1) in vec2 aTex;
            uniform mat4 view;
            uniform mat4 projection;
            uniform mat4 model;
            uniform vec2 uvOffset;
            uniform float cloudScale;
            out vec2 vTex;
            out vec3 FragPos; 
            void main() {
                vec4 worldPos = model * vec4(aPos, 1.0);
                gl_Position = projection * view * worldPos;
                FragPos = vec3(worldPos);
                vTex = aTex * cloudScale + uvOffset; 
            }
        """, """
            #version 330 core
            out vec4 FragColor;
            in vec2 vTex;
            in vec3 FragPos;
            
            uniform sampler2D cloudTex;
            uniform vec4 cloudColorTint;
            uniform float visibility;
            uniform vec3 viewPos;
            uniform float fogLimit; 

            vec2 rotate(vec2 uv, float angle) {
                float s = sin(angle);
                float c = cos(angle);
                mat2 rot = mat2(c, -s, s, c);
                return rot * uv;
            }

            void main() {
                // --- СЛОЙ 1: Основная форма ---
                vec4 col1 = texture(cloudTex, vTex);
                
                // --- СЛОЙ 2: Детали и "разбивание" сетки ---
                // Масштабируем на 0.6 (делаем крупнее) и поворачиваем на 1 радиан (~57 град)
                // Сдвигаем (vec2), чтобы не читать ту же точку текстуры
                vec2 uv2 = (vTex + vec2(10.5, 5.2)) * 0.6; 
                uv2 = rotate(uv2, 1.0); 
                vec4 col2 = texture(cloudTex, uv2);

                // --- СМЕШИВАНИЕ (Магия формы) ---
                // Перемножаем альфа-каналы и умножаем на 2.0.
                // Это оставляет облака только там, где оба слоя "белые", создавая сложные формы.
                float combinedAlpha = col1.a * col2.a * 2.0;
                
                // --- ПЛОТНОСТЬ (Soft Threshold) ---
                // 0.2 -> 0.7 дает мягкие края, но плотный центр
                float density = smoothstep(0.2, 0.7, combinedAlpha);

                if (density < 0.01) discard;

                // --- ТУМАН (Исчезновение на горизонте) ---
                float dist = length(FragPos - viewPos);
                // Начинаем исчезать на 50% дистанции, полностью исчезаем к 95%
                float fadeStart = fogLimit * 0.5;
                float fadeEnd = fogLimit * 0.95;
                float fogFactor = (fadeEnd - dist) / (fadeEnd - fadeStart);
                fogFactor = clamp(fogFactor, 0.0, 1.0);
                
                // Делаем исчезновение не линейным, а плавным (квадратичным)
                fogFactor = fogFactor * fogFactor;

                vec3 finalRGB = cloudColorTint.rgb;
                float alpha = density * visibility * fogFactor;
                
                FragColor = vec4(finalRGB, alpha);
            }
        """)
    def draw(self, view, proj, cam_pos, sun_angle_time, sun_tilt, sun_rot_y, day_intensity):
        rad_time = math.radians(sun_angle_time)
        rad_tilt = math.radians(sun_tilt)
        base_y = math.sin(rad_time)
        norm_factor = math.sqrt(1 + math.tan(rad_tilt)**2)
        h = base_y / norm_factor
        star_fade_start = -0.05 
        star_fade_full = -0.1  
        alpha = 0.0
        if h > star_fade_start:
            alpha = 0.0
        elif h < star_fade_full:
            alpha = 1.0
        else:
            alpha = (star_fade_start - h) / (star_fade_start - star_fade_full)
            alpha = alpha * alpha 
        if alpha <= 0.01: return
        self.shader.use()
        tilt_mat = MatrixUtils.rotation_x(sun_tilt)
        time_mat = MatrixUtils.rotation_x(sun_angle_time)
        rot_y_mat = MatrixUtils.rotation_y(sun_rot_y)
        model = rot_y_mat @ (time_mat @ tilt_mat)
        trans = MatrixUtils.translation(cam_pos[0], cam_pos[1], cam_pos[2])
        model = trans @ model
        self.shader.set_mat4("projection", proj)
        self.shader.set_mat4("view", view)
        self.shader.set_mat4("model", model)
        glUniform1f(glGetUniformLocation(self.shader.program, "starAlpha"), alpha)
        glUniform3f(glGetUniformLocation(self.shader.program, "starColor"), 1.0, 1.0, 1.0)
        glEnable(GL_PROGRAM_POINT_SIZE)
        try: glEnable(0x8861) 
        except: pass
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE) 
        glDepthMask(False) 
        glBindVertexArray(self.vao)
        glDrawArrays(GL_POINTS, 0, self.count)
        glBindVertexArray(0)
        glDepthMask(True)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glDisable(GL_PROGRAM_POINT_SIZE)
class ExportManager:
    @staticmethod
    def export_scene(filename, scene_obj, texture_manager, floor_chunk_size=10.0):
        print(f"Starting export to {filename}...")
        scene_export = trimesh.Scene()
        holes_bboxes = []
        for ent in scene_obj.entities:
            if ent.is_hole:
                holes_bboxes.append(ent.get_aabb())
                continue
            mesh = trimesh.creation.box(extents=ent.scale)
            mesh.apply_translation(ent.pos)
            col = ent.faces_colors[2] 
            r, g, b = col[0], col[1], col[2]
            a = col[3] if len(col) > 3 else 1.0
            reflect = ent.faces_reflectivity[2] if hasattr(ent, 'faces_reflectivity') else 0.0
            gloss = col[5] if len(col) > 5 else 0.0
            pbr = trimesh.visual.material.PBRMaterial(
                roughnessFactor=1.0 - gloss,
                metallicFactor=reflect,
                alphaMode='BLEND' if a < 0.99 or ent.density < 1.0 else 'OPAQUE',
                baseColorFactor=[r, g, b, a],
                doubleSided=False
            )
            tex_path = ent.faces_textures[2]
            if tex_path and os.path.exists(tex_path):
                try:
                    pil_img = Image.open(tex_path).convert("RGBA")
                    pbr.baseColorTexture = pil_img
                except: pass
            mesh.visual.material = pbr
            mesh.visual.face_colors = np.array([r*255, g*255, b*255, a*255], dtype=np.uint8)
            scene_export.add_geometry(mesh)
        used_coords = set()
        for ent in scene_obj.entities:
            cx = int(ent.pos[0] // floor_chunk_size)
            cz = int(ent.pos[2] // floor_chunk_size)
            used_coords.add((cx, cz))
        
        floor_polys = []
        
        if used_coords:
            floor_chunk_coords = set()
            # Бордюр 1 чанк вокруг
            for (cx, cz) in used_coords:
                for dx in range(-1, 2):
                    for dz in range(-1, 2):
                        floor_chunk_coords.add((cx + dx, cz + dz))
            
            # Заливка пустот внутри (Gap Filling)
            if floor_chunk_coords:
                min_x = min(c[0] for c in floor_chunk_coords)
                max_x = max(c[0] for c in floor_chunk_coords)
                min_z = min(c[1] for c in floor_chunk_coords)
                max_z = max(c[1] for c in floor_chunk_coords)
                
                for x in range(min_x, max_x + 1):
                    for z in range(min_z, max_z + 1):
                        if (x, z) in floor_chunk_coords: continue
                        has_left  = any((x - i, z) in used_coords for i in range(1, 4))
                        has_right = any((x + i, z) in used_coords for i in range(1, 4))
                        has_up    = any((x, z + i) in used_coords for i in range(1, 4))
                        has_down  = any((x, z - i) in used_coords for i in range(1, 4))
                        if (has_left and has_right) or (has_up and has_down):
                            floor_chunk_coords.add((x, z))

            # Создаем 2D полигоны для каждого чанка
            for (cx, cz) in floor_chunk_coords:
                x0 = cx * floor_chunk_size
                z0 = cz * floor_chunk_size
                x1 = x0 + floor_chunk_size
                z1 = z0 + floor_chunk_size
                floor_polys.append(shapely_box(x0, z0, x1, z1))

        if floor_polys:
            try:
                # 1. Объединяем чанки (быстро в 2D)
                floor_2d = unary_union(floor_polys)
                
                # 2. Вырезаем дырки (быстро в 2D)
                if holes_bboxes:
                    hole_rects = []
                    for (min_p, max_p) in holes_bboxes:
                        hole_rects.append(shapely_box(min_p[0], min_p[2], max_p[0], max_p[2]))
                    if hole_rects:
                        holes_2d = unary_union(hole_rects)
                        floor_2d = floor_2d.difference(holes_2d)
                
                # 3. Экструзия (выдавливание) в 3D
                # trimesh выдавливает по оси Z (высота). Получаем (X, Y_shapely, Z_height)
                full_floor = trimesh.creation.extrude_polygon(floor_2d, height=0.5)
                
                # 4. Поворачиваем оси, чтобы пол "лег" (Anterio Y-up)
                # Old X -> New X
                # Old Y (shapely Z) -> New Z
                # Old Z (height) -> New Y
                verts = full_floor.vertices
                new_verts = np.column_stack((verts[:, 0], verts[:, 2], verts[:, 1]))
                
                # Смещаем по Y вниз (0.0 -> -0.5)
                new_verts[:, 1] -= 0.5
                full_floor.vertices = new_verts
                full_floor.fix_normals()
                
                # 5. Красим и добавляем
                gr, gg, gb = COLOR_GROUND
                full_floor.visual.face_colors = np.array([gr*255, gg*255, gb*255, 255], dtype=np.uint8)
                floor_mat = trimesh.visual.material.PBRMaterial(
                    roughnessFactor=1.0, metallicFactor=0.0, 
                    baseColorFactor=[gr, gg, gb, 1.0]
                )
                full_floor.visual.material = floor_mat
                scene_export.add_geometry(full_floor)
            except Exception as e:
                print(f"Floor generation error: {e}")
        ext = os.path.splitext(filename)[1].lower()
        export_args = {}
        if ext == '.obj':
            export_args['include_normals'] = True
        if scene_export.is_empty:
            print("Export canceled: Scene is empty.")
            return False
        try:
            result = scene_export.export(filename, **export_args)
            if isinstance(result, (bytes, bytearray)):
                with open(filename, 'wb') as f:
                    f.write(result)
        except Exception as e:
            print(f"EXPORT ERROR: {e}")
            return False
        print("Export success.")
        return True
def lerp(a, b, t):
    return a + (b - a) * t

def lerp_angle(a, b, t):
    """Интерполяция углов с учетом перехода через 360/0"""
    diff = (b - a + 180) % 360 - 180
    return a + diff * t

def catmull_rom(p0, p1, p2, p3, t, tension1=0.5, tension2=0.5):
    """
    Сплайн Катмулла-Рома с раздельным контролем натяжения.
    tension1: натяжение в точке p1 (выход из начала сегмента).
    tension2: натяжение в точке p2 (вход в конец сегмента).
    """
    # Касательная в p1 зависит от tension1
    m0 = (p2 - p0) * (1.0 - tension1)
    
    # Касательная в p2 зависит от tension2
    m1 = (p3 - p1) * (1.0 - tension2)
    
    t2 = t * t
    t3 = t2 * t
    
    # Полиномы Эрмита
    h00 = 2*t3 - 3*t2 + 1
    h10 = t3 - 2*t2 + t
    h01 = -2*t3 + 3*t2
    h11 = t3 - t2
    
    return h00 * p1 + h10 * m0 + h01 * p2 + h11 * m1
class CameraKeyframe:
    def __init__(self, pos, yaw, pitch, time):
        self.pos = np.array(pos, dtype=np.float32)
        self.yaw = float(yaw)
        self.pitch = float(pitch)
        self.time = float(time)
        
        # Настройки сглаживания
        self.tension = 1.0     # 0.0 (круглый) -> 1.0 (прямой)
        self.continuity = 1.0   # 0.0 (линейная скорость) -> 1.0 (плавный старт/стоп)
    def to_dict(self):
        return {
            "pos": self.pos.tolist(),
            "yaw": self.yaw,
            "pitch": self.pitch,
            "time": self.time,
            "tension": self.tension,
            "continuity": self.continuity
        }

    @staticmethod
    def from_dict(data):
        kf = CameraKeyframe(
            data["pos"], 
            data["yaw"], 
            data["pitch"], 
            data["time"]
        )
        kf.tension = data.get("tension", 0.5)
        kf.continuity = data.get("continuity", 1.0) 
        return kf

class CameraPath:
    def __init__(self):
        self.keyframes = []
        self.is_looped = False
        self.loop_duration = 0.0 # ИСПРАВЛЕНО: было 5.0, теперь 0.0
        self.baked_lines = [] # Список кортежей (p1, p2, color)
        self.undo_stack = []
        self.redo_stack = []
    def add_keyframe(self, pos, yaw, pitch, time):
        # Если это не первый кадр, время не может быть меньше последнего
        if self.keyframes and time < self.keyframes[-1].time:
            time = self.keyframes[-1].time + 1.0
            
        kf = CameraKeyframe(pos, yaw, pitch, time)
        self.keyframes.append(kf)
        self.sort_frames()
        return kf
        
    def remove_keyframe(self, index):
        if 0 <= index < len(self.keyframes):
            self.keyframes.pop(index)
            
    def sort_frames(self):
        self.keyframes.sort(key=lambda k: k.time)
        
    def get_total_duration(self):
        if not self.keyframes: return 0.0
        dur = self.keyframes[-1].time
        if self.is_looped:
            dur += self.loop_duration
        return dur

    def to_dict(self):
        return {
            "keyframes": [kf.to_dict() for kf in self.keyframes],
            "is_looped": self.is_looped,
            "loop_duration": self.loop_duration
        }
    def bake_visualization(self):
        self.baked_lines = []
        if len(self.keyframes) < 2: return

        # 1. Считаем длины сегментов и общую дистанцию
        total_points = len(self.keyframes)
        if not self.is_looped: total_points -= 1
        
        # Настройки точности
        steps_per_segment = 20
        
        # Временные структуры
        path_points = [] # (pos, distance_from_start, segment_index)
        current_dist = 0.0
        
        # Проход 1: Генерация точек и расчет дистанции
        path_points.append( (self.keyframes[0].pos, 0.0, 0) )
        
        kf_centers = [] # Дистанция до центра каждого сегмента
        kf_speeds = []  # Скорость (continuity) каждого сегмента (берем из начала отрезка)
        
        for i in range(total_points):
            k1 = self.keyframes[i]
            k2 = self.keyframes[(i + 1) % len(self.keyframes)]
            
            # Для сплайна нужны 4 точки
            if i == 0 and not self.is_looped: k0 = k1
            else: k0 = self.keyframes[(i - 1) % len(self.keyframes)]
            
            if not self.is_looped and i == total_points - 1: k3 = k2
            else: k3 = self.keyframes[(i + 2) % len(self.keyframes)]

            # Скорость сегмента определяется параметром time кадра (duration = k2.time - k1.time)
            # Но для скорости нам нужно расстояние.
            # Сначала строим геометрию, чтобы узнать длину.
            
            segment_start_dist = current_dist
            prev_pos = k1.pos
            
            for s in range(1, steps_per_segment + 1):
                t = s / steps_per_segment
                # Используем существующую логику сплайна для позиции
                # tension берем из k1
                pos = catmull_rom(k0.pos, k1.pos, k2.pos, k3.pos, t, k1.tension, k2.tension)
                
                dist_step = np.linalg.norm(pos - prev_pos)
                current_dist += dist_step
                
                path_points.append( (pos, current_dist, i) )
                prev_pos = pos
            
            segment_len = current_dist - segment_start_dist
            kf_centers.append(segment_start_dist + segment_len / 2.0)
            
            # Расчет базовой скорости сегмента (Distance / Time)
            # Duration берем из разницы времени кадров
            dt = k2.time - k1.time
            if self.is_looped and i == len(self.keyframes) - 1:
                dt = self.loop_duration
            
            base_speed = segment_len / dt if dt > 0.001 else 0.0
            kf_speeds.append(base_speed)

        # Проход 2: Расчет скоростей в каждой точке и поиск Min/Max
        velocities = []
        min_v = float('inf')
        max_v = float('-inf')

        for p_idx in range(len(path_points)):
            pos, dist, seg_idx = path_points[p_idx]
            
            # Базовая скорость (ступенчатая)
            step_vel = kf_speeds[seg_idx]
            
            # Сглаженная скорость (интерполяция по центрам)
            # Находим центры слева и справа
            center_curr = kf_centers[seg_idx]
            
            # Определяем соседей для интерполяции
            if dist < center_curr:
                # Мы в левой половине сегмента -> интерполируем с предыдущим
                idx_a = seg_idx - 1
                idx_b = seg_idx
            else:
                # Мы в правой половине -> интерполируем со следующим
                idx_a = seg_idx
                idx_b = seg_idx + 1
            
            # Обработка границ пути
            valid_interpolation = True
            if not self.is_looped:
                if idx_a < 0: 
                    smooth_vel = kf_speeds[0]
                    valid_interpolation = False
                elif idx_b >= len(kf_speeds):
                    smooth_vel = kf_speeds[-1]
                    valid_interpolation = False
            
            if valid_interpolation:
                # Зацикливание индексов
                idx_a %= len(kf_speeds)
                idx_b %= len(kf_speeds)
                
                dist_a = kf_centers[idx_a]
                dist_b = kf_centers[idx_b]
                
                # Коррекция дистанции для зацикливания
                curr_d_temp = dist
                if self.is_looped:
                    if idx_a == len(kf_speeds) - 1 and idx_b == 0:
                        # Переход через конец цикла
                        if curr_d_temp < dist_a: curr_d_temp += current_dist # current_dist тут = total_length
                        dist_b += current_dist
                
                factor = (curr_d_temp - dist_a) / (dist_b - dist_a) if (dist_b - dist_a) > 0.001 else 0.0
                factor = max(0.0, min(1.0, factor))
                
                # SmoothStep для плавности
                factor = factor * factor * (3.0 - 2.0 * factor)
                
                vel_a = kf_speeds[idx_a]
                vel_b = kf_speeds[idx_b]
                smooth_vel = vel_a + (vel_b - vel_a) * factor

            # Смешивание (Continuity)
            # Берем continuity из текущего кадра (seg_idx)
            # В UI 0% = 1.0 (smooth), 100% = 0.0 (sharp). 
            # В данных continuity хранится как есть. 
            # ТЗ: "0 по умолчанию у новой камеры" (значит 0 это Sharp/Step).
            # Ранее мы договорились: continuity 1.0 = smooth default.
            # Давайте использовать значение continuity как factor смешивания:
            # 0.0 = Полностью Step, 1.0 = Полностью Smooth.
            
            k_obj = self.keyframes[seg_idx]
            blend = k_obj.continuity # Ожидается 0..1
            
            final_vel = step_vel * (1.0 - blend) + smooth_vel * blend
            
            velocities.append(final_vel)
            if final_vel < min_v: min_v = final_vel
            if final_vel > max_v: max_v = final_vel

        # Проход 3: Генерация линий с цветом
        if max_v - min_v < 0.001: max_v = min_v + 1.0 # Защита от деления на 0
        
        for i in range(len(path_points) - 1):
            p1 = path_points[i][0]
            p2 = path_points[i+1][0]
            vel = velocities[i]
            
            # Нормализация 0..1
            t = (vel - min_v) / (max_v - min_v)
            
            # Интерполяция цвета (Синий -> Розовый)
            c_min = np.array(COLOR_VELOCITY_MIN)
            c_max = np.array(COLOR_VELOCITY_MAX)
            col_rgb = c_min + (c_max - c_min) * t
            
            # Добавляем альфа-канал
            color = (col_rgb[0], col_rgb[1], col_rgb[2], 1.0)
            self.baked_lines.append((p1, p2, color))
    @staticmethod
    def from_dict(data):
        path = CameraPath()
        path.is_looped = data.get("is_looped", False)
        path.loop_duration = data.get("loop_duration", 0.0) # И тут тоже 0.0
        kf_list = data.get("keyframes", [])
        for kf_data in kf_list:
            path.keyframes.append(CameraKeyframe.from_dict(kf_data))
        path.sort_frames()
        return path
    def create_snapshot(self):
        # Сохраняем состояние как словарь (глубокая копия через to_dict)
        return self.to_dict()

    def restore_snapshot(self, data):
        # Восстанавливаем состояние из словаря
        self.keyframes = [CameraKeyframe.from_dict(k) for k in data['keyframes']]
        self.is_looped = data['is_looped']
        self.loop_duration = data['loop_duration']
        self.bake_visualization() # Сразу пересчитываем линии
    def get_interpolated_state(self, t):
        if not self.keyframes:
            return np.zeros(3), 0.0, 0.0
        
        count = len(self.keyframes)
        if count == 1:
            k = self.keyframes[0]
            return k.pos, k.yaw, k.pitch

        # 1. Зацикливание глобального времени
        total_dur = self.get_total_duration()
        if self.is_looped and total_dur > 0:
            t = t % total_dur
        else:
            if t <= self.keyframes[0].time:
                k = self.keyframes[0]
                return k.pos, k.yaw, k.pitch
            if t >= self.keyframes[-1].time:
                k = self.keyframes[-1]
                return k.pos, k.yaw, k.pitch

        # 2. Поиск текущего сегмента (idx)
        idx = -1
        for i in range(count - 1):
            if t >= self.keyframes[i].time and t < self.keyframes[i+1].time:
                idx = i
                break
        
        if idx == -1:
            if self.is_looped and t >= self.keyframes[-1].time:
                idx = count - 1
            else:
                idx = count - 2 if not self.is_looped else count - 1

        # 3. Определение соседей
        k1 = self.keyframes[idx]
        idx_next = (idx + 1) % count
        k2 = self.keyframes[idx_next]
        
        if idx == 0:
            k0 = self.keyframes[-1] if self.is_looped else k1
        else:
            k0 = self.keyframes[idx - 1]
            
        idx_next_next = (idx + 2) % count
        if not self.is_looped and (idx + 2) >= count:
            k3 = k2 
        else:
            k3 = self.keyframes[idx_next_next]

        # 4. Расчет длительностей (Time)
        if idx == count - 1:
            dt_curr = self.loop_duration
        else:
            dt_curr = k2.time - k1.time
            
        if dt_curr <= 0.0001: return k1.pos, k1.yaw, k1.pitch

        if idx == 0:
            dt_prev = self.loop_duration if self.is_looped else dt_curr
        else:
            dt_prev = k1.time - k0.time

        if idx == count - 1:
            dt_next = self.keyframes[1].time - self.keyframes[0].time
        elif idx == count - 2:
            dt_next = self.loop_duration if self.is_looped else dt_curr
        else:
            dt_next = k3.time - k2.time

        dt_prev = max(0.001, dt_prev)
        dt_next = max(0.001, dt_next)

        # === ГЛАВНОЕ ИСПРАВЛЕНИЕ: Физическая Скорость ===
        
        # Считаем расстояния (Dist)
        # Используем евклидово расстояние (по прямой) как хорошую аппроксимацию длины дуги
        dist_prev = np.linalg.norm(k1.pos - k0.pos)
        dist_curr = np.linalg.norm(k2.pos - k1.pos)
        dist_next = np.linalg.norm(k3.pos - k2.pos)

        # Считаем скорости (V = S / T)
        v_prev = dist_prev / dt_prev
        v_curr = dist_curr / dt_curr
        v_next = dist_next / dt_next

        # Если текущий сегмент нулевой длины (камера стоит), сглаживание не нужно
        if v_curr < 0.0001:
            slope_start = 1.0
            slope_end = 1.0
        else:
            # Целевая скорость в начале сегмента (среднее между предыдущей и текущей)
            # Если prev был медленный, а curr быстрый, v_start будет средним (разгон)
            v_start_target = (v_prev + v_curr) * 0.5
            
            # Целевая скорость в конце сегмента
            v_end_target = (v_curr + v_next) * 0.5

            # Коэффициенты наклона кривой времени (Slope)
            # Логика: Slope = V_target / V_average
            # Если Slope < 1, мы замедляем время (разгон). Если Slope > 1, ускоряем (торможение).
            slope_start = v_start_target / v_curr
            slope_end   = v_end_target   / v_curr

        # 5. Линейный прогресс
        u_lin = (t - k1.time) / dt_curr
        
        # 6. Hermite сплайн для времени (с учетом физических скоростей)
        v = u_lin
        v2 = v * v
        v3 = v2 * v
        
        u_smooth = (2.0 * v3 - 3.0 * v2 + 1.0) * 0.0 + \
                   (v3 - 2.0 * v2 + v) * slope_start + \
                   (-2.0 * v3 + 3.0 * v2) * 1.0 + \
                   (v3 - v2) * slope_end

        # Смешивание
        blend = k1.continuity
        u_final = u_lin * (1.0 - blend) + u_smooth * blend
        u_final = max(0.0, min(1.0, u_final))
        # 7. Интерполяция
        final_pos = catmull_rom(k0.pos, k1.pos, k2.pos, k3.pos, u_final, k1.tension, k2.tension)
        final_yaw = lerp_angle(k1.yaw, k2.yaw, u_final)
        final_pitch = lerp(k1.pitch, k2.pitch, u_final)
        
        return final_pos, final_yaw, final_pitch

class CameraManager:
    def __init__(self, app_ref):
        self.app = app_ref
        self.paths = [CameraPath() for _ in range(10)]
        self.active_slot = 0 
        
        self.selected_keyframes = set() 
        self.is_editing = False     
        
        self.backup_pos = None
        self.backup_rot = None
        self.hovered_kf = None 

        # --- Переменные для выделения рамкой (CAD style) ---
        self.rect_selecting = False
        self.rect_start = (0, 0)
        self.rect_current = (0, 0)
        self.is_modifying_continuous = False
    def push_undo(self):
        path = self.get_active_path()
        # Ограничим глубину стека (например, 50 шагов)
        if len(path.undo_stack) > 50:
            path.undo_stack.pop(0)
        
        # Создаем снимок и кладем в стек Undo
        snapshot = path.create_snapshot()
        path.undo_stack.append(snapshot)
        
        # Очищаем Redo при новом действии
        path.redo_stack.clear()
    def to_dict(self):
        return {
            "paths": [p.to_dict() for p in self.paths],
            "active_slot": self.active_slot
        }

    def from_dict(self, data):
        paths_data = data.get("paths", [])
        self.paths = []
        for i in range(10):
            if i < len(paths_data):
                self.paths.append(CameraPath.from_dict(paths_data[i]))
            else:
                self.paths.append(CameraPath())
        self.active_slot = data.get("active_slot", 0)
        for p in self.paths:
            p.bake_visualization()
        self.selected_keyframes = set()
        self.is_editing = False

    def get_active_path(self):
        return self.paths[self.active_slot]

    def _adjust_frame_duration(self, path, kf, delta):
        try:
            idx = path.keyframes.index(kf)
        except ValueError: return

        if idx == 0:
            path.loop_duration = max(0.0, path.loop_duration + delta)
            path.is_looped = (path.loop_duration > 0.1)
            return

        prev_kf = path.keyframes[idx - 1]
        current_duration = kf.time - prev_kf.time
        min_duration = 0.1
        new_duration = max(min_duration, current_duration + delta)
        actual_shift = new_duration - current_duration
        if abs(actual_shift) < 0.0001: return

        for i in range(idx, len(path.keyframes)):
            path.keyframes[i].time += actual_shift

    # --- Метод для получения 2D границ камеры (для выделения) ---
    def _get_keyframe_screen_aabb(self, kf):
        # Размер гизмо камеры (примерно 0.2 от центра)
        size = 0.2
        min_p = kf.pos - size
        max_p = kf.pos + size
        
        corners_3d = [
            [min_p[0], min_p[1], min_p[2]], [max_p[0], min_p[1], min_p[2]],
            [min_p[0], max_p[1], min_p[2]], [max_p[0], max_p[1], min_p[2]],
            [min_p[0], min_p[1], max_p[2]], [max_p[0], min_p[1], max_p[2]],
            [min_p[0], max_p[1], max_p[2]], [max_p[0], max_p[1], max_p[2]]
        ]
        
        xs, ys = [], []
        for p in corners_3d:
            # Используем функцию App для проекции
            res = self.app.project_point_to_screen(p[0], p[1], p[2])
            if res:
                xs.append(res[0])
                ys.append(res[1])
        
        if not xs: return None # Камера за экраном
        
        return min(xs), min(ys), max(xs), max(ys)

    def _perform_rect_selection(self, is_ctrl):
        x1, y1 = self.rect_start
        x2, y2 = self.rect_current
        
        # Определяем тип выделения
        # Left -> Right (x2 > x1): Window (синий, объект должен быть полностью внутри)
        # Right -> Left (x2 < x1): Crossing (зеленый, объект должен пересекать)
        is_crossing = (x1 > x2)
        
        r_min_x, r_max_x = min(x1, x2), max(x1, x2)
        r_min_y, r_max_y = min(y1, y2), max(y1, y2)
        
        path = self.get_active_path()
        new_selection = set()
        
        if is_ctrl:
            new_selection = self.selected_keyframes.copy()
        
        for kf in path.keyframes:
            aabb = self._get_keyframe_screen_aabb(kf)
            if not aabb: continue
            
            k_min_x, k_min_y, k_max_x, k_max_y = aabb
            
            if is_crossing:
                # Пересечение прямоугольников
                overlap_x = (r_min_x < k_max_x) and (r_max_x > k_min_x)
                overlap_y = (r_min_y < k_max_y) and (r_max_y > k_min_y)
                if overlap_x and overlap_y:
                    new_selection.add(kf)
            else:
                # Полное вхождение (Window)
                inside_x = (k_min_x >= r_min_x) and (k_max_x <= r_max_x)
                inside_y = (k_min_y >= r_min_y) and (k_max_y <= r_max_y)
                if inside_x and inside_y:
                    new_selection.add(kf)
                    
        self.selected_keyframes = new_selection

    def handle_input(self, event):
        path = self.get_active_path()
        keys = self.app.input.get_keys()
        is_ctrl = keys.get(sdl2.SDLK_LCTRL) or keys.get(sdl2.SDLK_RCTRL)
        is_alt = keys.get(sdl2.SDLK_LALT) or keys.get(sdl2.SDLK_RALT)
        is_shift = keys.get(sdl2.SDLK_LSHIFT) or keys.get(sdl2.SDLK_RSHIFT)

        # --- MOUSE MOTION (Обновление рамки) ---
        if event.type == sdl2.SDL_MOUSEMOTION:
            if self.rect_selecting:
                self.rect_current = (event.motion.x, event.motion.y)
                return True

        if event.type == sdl2.SDL_KEYDOWN:
            if event.key.repeat: return False 
            key = event.key.keysym.sym
            
            if key == sdl2.SDLK_s and is_ctrl and is_alt:
                self.app.quick_save()
                return True
            if key == sdl2.SDLK_z and is_ctrl:
                if path.undo_stack:
                    # 1. Запоминаем текущее состояние выделения
                    was_editing = self.is_editing
                    # Сохраняем индексы выбранных кадров (так как сами объекты будут заменены)
                    selected_indices = [path.keyframes.index(k) for k in self.selected_keyframes if k in path.keyframes]

                    # 2. Сохраняем текущее в Redo
                    path.redo_stack.append(path.create_snapshot())
                    
                    # 3. Восстанавливаем из Undo
                    state = path.undo_stack.pop()
                    path.restore_snapshot(state)
                    
                    # 4. Восстанавливаем выделение по индексам
                    self.selected_keyframes.clear()
                    for idx in selected_indices:
                        if idx < len(path.keyframes):
                            self.selected_keyframes.add(path.keyframes[idx])
                    
                    # 5. Восстанавливаем режим редактирования
                    # Если выбранных кадров не осталось или их стало > 1, редактирование сбрасывается
                    if was_editing and len(self.selected_keyframes) == 1:
                        self.is_editing = True
                        # ВАЖНО: Синхронизируем камеру игрока с восстановленным кадром
                        kf = list(self.selected_keyframes)[0]
                        self.app.camera.pos = np.copy(kf.pos)
                        self.app.camera.yaw = kf.yaw
                        self.app.camera.pitch = kf.pitch
                        self.app.camera.update_vectors()
                        # Обновляем бэкап позиции, чтобы ESC работал корректно относительно нового состояния
                        self.backup_pos = np.copy(kf.pos)
                        self.backup_rot = (kf.yaw, kf.pitch)
                    else:
                        self.is_editing = False

                    self.app.show_notification("UNDO (CAMERA)")
                    self.app.unsaved_changes = True
                return True
            # --------------------------------------

            # --- НОВОЕ: Локальный Redo (Ctrl+Y) ---
            if key == sdl2.SDLK_y and is_ctrl:
                if path.redo_stack:
                    # 1. Запоминаем состояние
                    was_editing = self.is_editing
                    selected_indices = [path.keyframes.index(k) for k in self.selected_keyframes if k in path.keyframes]

                    # 2. Сохраняем в Undo
                    path.undo_stack.append(path.create_snapshot())
                    
                    # 3. Восстанавливаем
                    state = path.redo_stack.pop()
                    path.restore_snapshot(state)
                    
                    # 4. Восстанавливаем выделение
                    self.selected_keyframes.clear()
                    for idx in selected_indices:
                        if idx < len(path.keyframes):
                            self.selected_keyframes.add(path.keyframes[idx])
                    
                    # 5. Восстанавливаем редактирование
                    if was_editing and len(self.selected_keyframes) == 1:
                        self.is_editing = True
                        kf = list(self.selected_keyframes)[0]
                        self.app.camera.pos = np.copy(kf.pos)
                        self.app.camera.yaw = kf.yaw
                        self.app.camera.pitch = kf.pitch
                        self.app.camera.update_vectors()
                        self.backup_pos = np.copy(kf.pos)
                        self.backup_rot = (kf.yaw, kf.pitch)
                    else:
                        self.is_editing = False

                    self.app.show_notification("REDO (CAMERA)")
                    self.app.unsaved_changes = True
                return True
            if sdl2.SDLK_1 <= key <= sdl2.SDLK_9:
                self.active_slot = key - sdl2.SDLK_1
                self.selected_keyframes.clear()
                self.is_editing = False
                self.app.unsaved_changes = True
                return True
            if key == sdl2.SDLK_0:
                self.active_slot = 9
                self.selected_keyframes.clear()
                self.is_editing = False
                self.app.unsaved_changes = True
                return True

            if key == sdl2.SDLK_ESCAPE:
                if self.is_editing:
                    # ... (код отмены редактирования) ...
                    if len(self.selected_keyframes) == 1:
                        kf = list(self.selected_keyframes)[0]
                        kf.pos = self.backup_pos
                        kf.yaw = self.backup_rot[0]
                        kf.pitch = self.backup_rot[1]
                        self.app.camera.pos = np.copy(kf.pos)
                        self.app.camera.yaw = kf.yaw
                        self.app.camera.pitch = kf.pitch
                        self.app.camera.update_vectors()
                    self.is_editing = False
                    self.app.show_notification("EDIT CANCELED")
                    return True
                
                # Если тянем рамку - отмена рамки
                if self.rect_selecting:
                    self.rect_selecting = False
                    self.app.set_mouse_lock(True)
                    return True
                
                # Если курсор просто отвязан - привязываем обратно
                if not self.app.mouse_locked:
                    self.app.set_mouse_lock(True)
                    return True

                if self.selected_keyframes:
                    self.selected_keyframes.clear()
                    return True
                return False 

            if is_shift and len(self.selected_keyframes) == 1 and not self.is_editing:
                # ... (код реордеринга Shift+Arrow без изменений) ...
                kf = list(self.selected_keyframes)[0]
                try: idx = path.keyframes.index(kf)
                except ValueError: return False
                swap_target_idx = -1
                if key == sdl2.SDLK_LEFT and idx > 0: swap_target_idx = idx - 1
                elif key == sdl2.SDLK_RIGHT and idx < len(path.keyframes) - 1: swap_target_idx = idx + 1
                if swap_target_idx != -1:
                    self.push_undo() 
                    target_kf = path.keyframes[swap_target_idx]
                    t1, t2 = kf.time, target_kf.time
                    if abs(t1 - t2) < 0.001:
                        if swap_target_idx > idx: t2 = t1 + 0.1
                        else: t2 = t1 - 0.1
                    kf.time = t2
                    target_kf.time = t1
                    path.sort_frames() 
                    self.app.unsaved_changes = True
                    return True

            if key == sdl2.SDLK_RETURN:
                # ... (код Enter без изменений) ...
                cam = self.app.camera
                if len(self.selected_keyframes) > 1:
                    self.app.show_notification("CANNOT EDIT POS OF MULTIPLE CAMERAS")
                    return True
                single_kf = list(self.selected_keyframes)[0] if len(self.selected_keyframes) == 1 else None
                if self.is_editing and single_kf:
                    self.push_undo() 
                    single_kf.pos = np.copy(cam.pos)
                    single_kf.yaw = cam.yaw
                    single_kf.pitch = cam.pitch
                    self.is_editing = False
                    self.app.show_notification("POSITION UPDATED")
                    path.bake_visualization() 
                    self.app.unsaved_changes = True
                    return True
                if single_kf and not self.is_editing:
                    self.backup_pos = np.copy(single_kf.pos)
                    self.backup_rot = (single_kf.yaw, single_kf.pitch)
                    cam.pos = np.copy(single_kf.pos)
                    cam.yaw = single_kf.yaw
                    cam.pitch = single_kf.pitch
                    cam.update_vectors()
                    self.is_editing = True
                    return True
                if not self.selected_keyframes:
                    self.push_undo() 
                    new_time = 0.0
                    if path.keyframes: new_time = path.keyframes[-1].time + 2.0
                    new_kf = path.add_keyframe(cam.pos, cam.yaw, cam.pitch, new_time)
                    new_kf.continuity = 0.0
                    path.bake_visualization() 
                    self.selected_keyframes.add(new_kf)
                    self.app.show_notification("KEYFRAME ADDED")
                    self.app.unsaved_changes = True 
                    return True

            if key == sdl2.SDLK_DELETE:
                # ... (код Delete без изменений) ...
                if self.selected_keyframes and not self.is_editing:
                    self.push_undo() 
                    for kf in list(self.selected_keyframes):
                        if kf in path.keyframes: path.keyframes.remove(kf)
                    path.bake_visualization() 
                    self.selected_keyframes.clear()
                    self.app.show_notification("KEYFRAMES DELETED")
                    self.app.unsaved_changes = True
                    return True

            if key == sdl2.SDLK_c and not is_ctrl:
                # ... (код Render без изменений) ...
                def on_render_confirm(filename):
                    if filename is None: 
                        self.app.set_mouse_lock(True)
                        return
                    self.app.render_video_sequence(filename)
                    self.app.set_mouse_lock(True)
                self.app.file_dialog.open('save', on_render_confirm, is_render=True)
                self.app.set_mouse_lock(False)
                return True
                
        if event.type == sdl2.SDL_MOUSEBUTTONDOWN:
            btn = event.button.button
            
            # --- СЦЕНАРИЙ 1: Мышь ЗАХВАЧЕНА (Полет) ---
            if self.app.mouse_locked:
                if btn == sdl2.SDL_BUTTON_LEFT:
                    # Одиночный выбор Raycast
                    if not self.is_editing:
                        if self.hovered_kf:
                            if is_ctrl:
                                if self.hovered_kf in self.selected_keyframes: self.selected_keyframes.remove(self.hovered_kf)
                                else: self.selected_keyframes.add(self.hovered_kf)
                            else: self.selected_keyframes = {self.hovered_kf}
                            return True
                        else:
                            if not is_ctrl: self.selected_keyframes.clear()
                            return True
                
                elif btn == sdl2.SDL_BUTTON_RIGHT:
                    # Просто отвязываем мышь
                    self.app.set_mouse_lock(False)
                    return True

            # --- СЦЕНАРИЙ 2: Мышь ОТВЯЗАНА (Курсор) ---
            else:
                # Любая кнопка начинает выделение рамкой
                if btn in [sdl2.SDL_BUTTON_LEFT, sdl2.SDL_BUTTON_RIGHT]:
                    if not self.is_editing:
                        self.rect_selecting = True
                        self.rect_start = (event.button.x, event.button.y)
                        self.rect_current = (event.button.x, event.button.y)
                        return True

        if event.type == sdl2.SDL_MOUSEBUTTONUP:
            # Завершение рамки
            if self.rect_selecting:
                self._perform_rect_selection(is_ctrl)
                self.rect_selecting = False
                # Сразу привязываем обратно (как в ТЗ)
                self.app.set_mouse_lock(True)
                return True

        return False

    def update(self, dt, ray_origin, ray_dir):
        # 1. Логика непрерывного изменения параметров (Duration, Ease, Smoothing)
        if self.selected_keyframes and not self.is_editing:
            path = self.get_active_path()
            keys = self.app.input.get_keys()
            
            # --- ИСПРАВЛЕНИЕ: Надежное определение модификаторов ---
            # Используем GetModState, чтобы точно знать, зажат ли Ctrl, 
            # даже если событие нажатия было пропущено.
            mod_state = sdl2.SDL_GetModState()
            is_ctrl = (mod_state & sdl2.KMOD_CTRL) != 0
            is_shift = (mod_state & sdl2.KMOD_SHIFT) != 0
            # -------------------------------------------------------
            
            # Определяем, пытается ли пользователь что-то менять прямо сейчас
            is_changing_now = False
            
            # Shift используется для реордеринга, он не влияет на непрерывные параметры
            if not is_shift:
                # Проверяем нажатие стрелок
                if keys.get(sdl2.SDLK_UP) or keys.get(sdl2.SDLK_DOWN):
                    is_changing_now = True
                
                # Если зажат Ctrl, то влево/вправо тоже меняют параметры
                if is_ctrl and (keys.get(sdl2.SDLK_LEFT) or keys.get(sdl2.SDLK_RIGHT)):
                    is_changing_now = True

            # --- ЛОГИКА UNDO ДЛЯ НЕПРЕРЫВНЫХ ДЕЙСТВИЙ ---
            if is_changing_now:
                # Если мы только начали нажимать клавиши - сохраняем состояние "ДО"
                if not self.is_modifying_continuous:
                    self.push_undo()
                    self.is_modifying_continuous = True
            else:
                # Клавиши отпущены - сбрасываем флаг, чтобы следующее нажатие создало новый Undo
                self.is_modifying_continuous = False
            # ----------------------------------------------

            # Если происходит изменение, вычисляем и применяем значения
            if is_changing_now:
                changed = False
                time_speed = 1.0 * dt
                param_speed = 0.5 * dt
                
                d_time = 0.0
                d_tension = 0.0
                d_continuity = 0.0
                
                if not is_ctrl:
                    if keys.get(sdl2.SDLK_UP): d_time = time_speed
                    if keys.get(sdl2.SDLK_DOWN): d_time = -time_speed
                else:
                    if keys.get(sdl2.SDLK_LEFT): d_tension = param_speed
                    if keys.get(sdl2.SDLK_RIGHT): d_tension = -param_speed
                    if keys.get(sdl2.SDLK_UP): d_continuity = param_speed
                    if keys.get(sdl2.SDLK_DOWN): d_continuity = -param_speed

                if d_time != 0:
                    sorted_kfs = sorted(list(self.selected_keyframes), key=lambda k: path.keyframes.index(k))
                    rep_kf = sorted_kfs[0]
                    rep_idx = path.keyframes.index(rep_kf)
                    
                    if rep_idx == 0: 
                        current_rep_dur = path.loop_duration
                    else:
                        prev_rep = path.keyframes[rep_idx - 1]
                        current_rep_dur = rep_kf.time - prev_rep.time
                    
                    min_limit = 0.0 if rep_idx == 0 else 0.1
                    target_dur = max(min_limit, current_rep_dur + d_time)
                    
                    for kf in sorted_kfs:
                        k_idx = path.keyframes.index(kf)
                        if k_idx == 0: curr_dur = path.loop_duration
                        else: curr_dur = kf.time - path.keyframes[k_idx - 1].time
                        
                        diff = target_dur - curr_dur
                        if abs(diff) > 0.0001:
                            self._adjust_frame_duration(path, kf, diff)
                    changed = True

                if d_tension != 0 or d_continuity != 0:
                    for kf in self.selected_keyframes:
                        if d_tension != 0: kf.tension = max(0.0, min(1.0, kf.tension + d_tension))
                        if d_continuity != 0: kf.continuity = max(0.0, min(2.0, kf.continuity + d_continuity))
                    changed = True

                if changed:
                    path.bake_visualization() 
                    self.app.unsaved_changes = True

        # 2. Обновление наведения мыши
        if self.is_editing: 
            self.hovered_kf = None
            return

        path = self.get_active_path()
        best_dist = 100.0 
        best_kf = None
        for kf in path.keyframes:
            v = kf.pos - ray_origin
            t = np.dot(v, ray_dir)
            if t > 0: 
                closest_point_on_ray = ray_origin + ray_dir * t
                dist_to_kf = np.linalg.norm(closest_point_on_ray - kf.pos)
                if dist_to_kf < 0.5 and t < best_dist:
                    best_dist = t
                    best_kf = kf
        self.hovered_kf = best_kf

    def render_world(self, view_mat, proj_mat, cam_pos):
        renderer = self.app.line_renderer
        
        # 1. Неактивные пути (рисуем серым, берем геометрию из кэша)
        for i, p in enumerate(self.paths):
            if i == self.active_slot: continue
            if len(p.keyframes) < 2: continue
            
            # Если кэш пуст (например, при загрузке), считаем его
            if not p.baked_lines: p.bake_visualization()
            
            # Рисуем тусклым серым, игнорируя цвет скорости
            col = (0.5, 0.5, 0.5, 0.2)
            for p1, p2, _ in p.baked_lines:
                renderer.add_line(p1, p2, col)
            inactive_cam_col = (0.4, 0.4, 0.4, 0.4) # Серый полупрозрачный
            for kf in p.keyframes:
                self._draw_camera_gizmo(renderer, kf.pos, kf.yaw, kf.pitch, inactive_cam_col)
        
        # 2. Активный путь (рисуем с градиентом скорости)
        path = self.get_active_path()
        if len(path.keyframes) >= 2:
            # Если кэш пуст, считаем его
            if not path.baked_lines: path.bake_visualization()
            
            # Рисуем линии, используя цвет из baked_lines (он там уже рассчитан: синий->розовый)
            for p1, p2, color in path.baked_lines:
                renderer.add_line(p1, p2, color)
        
        # 3. Гизмо камер (остается без изменений, как было)
        for i, kf in enumerate(path.keyframes):
            is_selected = (kf in self.selected_keyframes)
            is_hovered = (kf == self.hovered_kf)
            is_editing = (is_selected and self.is_editing)
            
            if is_editing: col = (1.0, 0.0, 0.0, 1.0)
            elif is_selected: col = (1.0, 1.0, 0.0, 1.0)
            elif is_hovered: col = (1.0, 1.0, 0.5, 1.0)
            elif i == 0 and path.is_looped: col = (0.0, 1.0, 0.0, 1.0)
            else: col = (1.0, 1.0, 1.0, 0.8)
            
            if is_editing:
                self._draw_camera_gizmo(renderer, self.app.camera.pos, self.app.camera.yaw, self.app.camera.pitch, col)
            else:
                self._draw_camera_gizmo(renderer, kf.pos, kf.yaw, kf.pitch, col)
        
        renderer.flush(view_mat, proj_mat, line_width=2.0)

    def _draw_camera_gizmo(self, renderer, pos, yaw, pitch, color):
        rad_y = math.radians(yaw); rad_p = math.radians(pitch)
        fx = math.cos(rad_y) * math.cos(rad_p)
        fy = math.sin(rad_p)
        fz = math.sin(rad_y) * math.cos(rad_p)
        fwd = np.array([fx, fy, fz], dtype=np.float32)
        up = np.array([0, 1, 0], dtype=np.float32)
        right = np.cross(fwd, up)
        real_up = np.cross(right, fwd)
        
        # Более компактный гизмо
        renderer.add_box_with_diagonals(pos - 0.1, pos + 0.1, color)
        renderer.add_line(pos, pos + fwd * 0.5, color) # Короче линза
        
        frustum_end = pos + fwd * 0.3
        w, h = right * 0.15, real_up * 0.1
        p1 = frustum_end - w - h; p2 = frustum_end + w - h
        p3 = frustum_end + w + h; p4 = frustum_end - w + h
        
        renderer.add_line(pos, p1, color); renderer.add_line(pos, p2, color)
        renderer.add_line(pos, p3, color); renderer.add_line(pos, p4, color)
        renderer.add_line(p1, p2, color); renderer.add_line(p2, p3, color)
        renderer.add_line(p3, p4, color); renderer.add_line(p4, p1, color)

    def draw_ui(self, proj_mat):
        w, h = self.app.win_w, self.app.win_h
        
        # --- ОТРИСОВКА РАМКИ ВЫДЕЛЕНИЯ ---
        if self.rect_selecting:
            x1, y1 = self.rect_start
            x2, y2 = self.rect_current
            
            # Определение типа выделения для цвета
            if x1 > x2: # Right -> Left (Crossing)
                col_fill = (0.0, 1.0, 0.0, 0.2)
                col_border = (0.0, 1.0, 0.0, 0.8)
            else: # Left -> Right (Window)
                col_fill = (0.0, 0.0, 1.0, 0.2)
                col_border = (0.0, 0.0, 1.0, 0.8)
            
            min_x, max_x = min(x1, x2), max(x1, x2)
            min_y, max_y = min(y1, y2), max(y1, y2)
            width_r = max_x - min_x
            height_r = max_y - min_y
            
            # Рисуем
            self.app.solid_renderer.add_quad_2d(min_x, min_y, width_r, height_r, col_fill)
            self.app.solid_renderer.flush(MatrixUtils.identity(), proj_mat)
            
            # Рамка
            p1 = [min_x, min_y, 0]; p2 = [max_x, min_y, 0]
            p3 = [max_x, max_y, 0]; p4 = [min_x, max_y, 0]
            self.app.line_renderer.add_line(p1, p2, col_border)
            self.app.line_renderer.add_line(p2, p3, col_border)
            self.app.line_renderer.add_line(p3, p4, col_border)
            self.app.line_renderer.add_line(p4, p1, col_border)
            self.app.line_renderer.flush(MatrixUtils.identity(), proj_mat)

        slot_text = f"{self.app.tr('CAM_MODE')} | {self.app.tr('CAM_SLOT')}: {self.active_slot + 1}"
        if self.is_editing: slot_text += f" {self.app.tr('CAM_EDITING')}"
        elif self.app.input.keys.get(sdl2.SDLK_LCTRL): slot_text += f" {self.app.tr('CAM_SMOOTH')}"
        
        path = self.get_active_path()
        dur = path.get_total_duration()
        
        # ИСПРАВЛЕНИЕ 1: Перевод ON/OFF
        loop_st = self.app.tr('CAM_ON') if path.is_looped else self.app.tr('CAM_OFF')
        
        # ИСПРАВЛЕНИЕ 2: Перевод 's' (секунды)
        sec_str = self.app.tr('CAM_SEC')

        info_lines = [
            slot_text,
            # Здесь тоже добавляем sec_str
            f"{self.app.tr('CAM_TOTAL')}: {dur:.1f}{sec_str} | {self.app.tr('CAM_KEYS')}: {len(path.keyframes)} | {self.app.tr('CAM_LOOP')}: {loop_st}",
            self.app.tr('CAM_HINT_1'),
            self.app.tr('CAM_HINT_2'),
            self.app.tr('CAM_HINT_3')
        ]
        
        y_off = 20
        for line in info_lines:
            tex, tw, th = safe_text_to_texture(line, self.app.font, (255, 255, 255))
            if tex:
                self.app.sprite_renderer.draw_ui_sprite(tex, 20, y_off, tw, th, proj_mat)
                glDeleteTextures([tex])
                y_off += 30
        
        if self.selected_keyframes:
            count = len(self.selected_keyframes)
            y_off = h - 180 
            
            sorted_sel = sorted(list(self.selected_keyframes), key=lambda k: k.time)
            repr_kf = sorted_sel[0]
            repr_idx = path.keyframes.index(repr_kf)
            
            # Вспомогательная переменная для 'с'
            sec_str = self.app.tr('CAM_SEC')

            if repr_idx == 0:
                dur_label = self.app.tr('CAM_LOOP_T')
                val = path.loop_duration
                val_str = f"{val:.1f}{sec_str}"
                
                # ИСПРАВЛЕНИЕ 3: Перевод (Off) для выключенного цикла
                if not path.is_looped: val_str += f" ({self.app.tr('CAM_OFF')})"
            else:
                dur_label = self.app.tr('CAM_DUR')
                prev_time = path.keyframes[repr_idx-1].time
                val = repr_kf.time - prev_time
                val_str = f"{val:.1f}{sec_str}"

            # ИСПРАВЛЕНИЕ 4: Перевод (+others)
            if count > 1: val_str += self.app.tr('CAM_OTHERS')

            if count == 1: header = f"{self.app.tr('CAM_SEL_ONE')} #{repr_idx + 1}"
            else: header = self.app.tr('CAM_SEL_MANY').format(count=count)

            ui_tension = int((1.0 - repr_kf.tension) * 100)
            ui_continuity = int((repr_kf.continuity / 2.0) * 100)

            # ИСПРАВЛЕНИЕ 5: Перевод Smoothness и Ease
            # Используем ключи, которые уже были в словаре, но не использовались
            props_str = f"{self.app.tr('CAM_SMOOTHNESS')}: {ui_tension}% | {self.app.tr('CAM_EASE')}: {ui_continuity}%"

            sel_lines = [
                (header, (255, 255, 0)),
                (f"{dur_label}: {val_str}", (0, 255, 255)), 
                (props_str, (200, 200, 200))
            ]
            
            if count == 1 and repr_idx > 0:
                sel_lines.insert(2, (f"({self.app.tr('CAM_AT')}: {repr_kf.time:.1f}{sec_str})", (150, 150, 150)))

            if self.app.input.keys.get(sdl2.SDLK_LSHIFT) and count == 1:
                sel_lines.append((self.app.tr('CAM_REORDER'), (150, 150, 150)))

            for txt, col in sel_lines:
                # ... (код отрисовки без изменений) ...
                tex, tw, th = safe_text_to_texture(txt, self.app.font, col)
                if tex:
                    self.app.sprite_renderer.draw_ui_sprite(tex, 20, y_off, tw, th, proj_mat)
                    glDeleteTextures([tex])
                    y_off += 30
        now = pygame.time.get_ticks()
        if now - self.app.notification_timer < 2000 and self.app.notification_text:
            # Зеленая плашка фона сверху
            self.app.solid_renderer.add_quad_2d(0, 0, w, 40, (0.0, 0.5, 0.0, 0.8))
            self.app.solid_renderer.flush(MatrixUtils.identity(), proj_mat)
            
            # Текст уведомления
            tex, tw, th = safe_text_to_texture(self.app.notification_text, self.app.font, (255, 255, 255))
            if tex:
                self.app.sprite_renderer.draw_ui_sprite(tex, (w - tw)//2, (40 - th)//2, tw, th, proj_mat)
                glDeleteTextures([tex])
class App:
    def __init__(self):
        pygame.init()
        self._init_core_systems()
        self.last_stable_pos = np.array([0.0, 1.8, 0.0], dtype=np.float32) 
        self.input = InputManager()
        sdl2.SDL_StartTextInput()
        self._init_graphics()
        self._init_resources()
        self._init_game_state()
        self._init_scene_objects()
        self.create_ui()
        self.cine_cam = CameraManager(self)
        self.is_rendering_video = False
        self.was_in_cinecam = False
        if hasattr(self, 'color_picker'):
            self.color_picker.update_position(self.win_w - 320, 100, self.win_h)
        if hasattr(self, 'file_dialog'):
            self.file_dialog.update_layout(self.win_w, self.win_h, self.font)
        self.file_dialog.tr_func = self.tr
        self.build_spatial_grid()
        self.update_chunks(force_radius=True, render_radius=12)
    def _init_core_systems(self):
        if sdl2.SDL_Init(sdl2.SDL_INIT_VIDEO) != 0:
            raise RuntimeError(sdl2.SDL_GetError())
        sdl2.SDL_GL_SetAttribute(sdl2.SDL_GL_CONTEXT_MAJOR_VERSION, 3)
        sdl2.SDL_GL_SetAttribute(sdl2.SDL_GL_CONTEXT_MINOR_VERSION, 3)
        sdl2.SDL_GL_SetAttribute(sdl2.SDL_GL_CONTEXT_PROFILE_MASK, sdl2.SDL_GL_CONTEXT_PROFILE_COMPATIBILITY)
        sdl2.SDL_GL_SetAttribute(sdl2.SDL_GL_DOUBLEBUFFER, 1)
        sdl2.SDL_GL_SetAttribute(sdl2.SDL_GL_DEPTH_SIZE, 24)
        sdl2.SDL_GL_SetAttribute(sdl2.SDL_GL_STENCIL_SIZE, 8)
        self.window = sdl2.SDL_CreateWindow(
            b"Anterio",
            sdl2.SDL_WINDOWPOS_CENTERED, sdl2.SDL_WINDOWPOS_CENTERED,
            WINDOW_SIZE[0], WINDOW_SIZE[1],
            sdl2.SDL_WINDOW_OPENGL | sdl2.SDL_WINDOW_RESIZABLE
        )
        if not self.window:
            raise RuntimeError(sdl2.SDL_GetError())
        sdl2.SDL_SetWindowMinimumSize(self.window, 960, 720)
        self.gl_context = sdl2.SDL_GL_CreateContext(self.window)
        self.limit_fps = True
        sdl2.SDL_GL_SetSwapInterval(1 if self.limit_fps else 0)
        dw, dh = ctypes.c_int(), ctypes.c_int()
        ww, wh = ctypes.c_int(), ctypes.c_int()
        sdl2.SDL_GL_GetDrawableSize(self.window, dw, dh)
        sdl2.SDL_GetWindowSize(self.window, ww, wh)
        self.draw_w, self.draw_h = dw.value, dh.value
        self.win_w, self.win_h = ww.value, wh.value
        self.fullscreen = False
        glViewport(0, 0, self.draw_w, self.draw_h)
        self.clock = pygame.time.Clock()
        self.baseline_fps = 60.0
    def _init_graphics(self):
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_CULL_FACE)
        glClearColor(*COLOR_SKY, 1.0)
        self.floor_renderer = DynamicFloorRenderer()
        self.shader = Shader(DEFAULT_VERT_SHADER, DEFAULT_FRAG_SHADER)
        self.reflection_fbos = [Framebuffer(self.draw_w, self.draw_h) for _ in range(MAX_MIRRORS)]
        self.texture_manager = TextureManager()
        self.cube_renderer = CubeRenderer(self.texture_manager)
        self.line_renderer = BatchRenderer(GL_LINES)      
        self.solid_renderer = BatchRenderer(GL_TRIANGLES) 
        self.sprite_renderer = SpriteRenderer()           
    def _init_resources(self):
        self.font = pygame.font.SysFont('Arial', 18)
        self.title_font = pygame.font.SysFont('Arial', 48)
        self.language = 'en'
        try:
            # ВОТ ЭТА СТРОКА ВЫЗЫВАЕТ ПРЕДУПРЕЖДЕНИЕ:
            sys_loc = locale.getdefaultlocale()[0]
            if sys_loc:
                sys_code = sys_loc.split('_')[0].lower()
                if sys_code in RU_LOCALES:
                    self.language = 'ru'
        except:
            pass
        print(f"System Language detected: {self.language}")
        self.tex_sun = create_circle_texture((255, 255, 200, 255), size=512, hardness=0.8, noise_strength=0.0)
        self.texture_manager = TextureManager()
        self.tex_moon = create_circle_texture((220, 220, 240, 255), size=512, hardness=0.8, noise_strength=0.3)
        self.noise_tex_id = create_noise_texture()
        self.grid_pattern_tex_id = create_grid_texture_pattern()
        self.light_icon_tex_id = create_light_icon_texture()
        self.cloud_tex_id = create_procedural_cloud_texture()
        self.cloud_renderer = CloudRenderer(self.cloud_tex_id)
        self.star_renderer = StarRenderer(count=3621) 
        self.label_pool = [TextLabel(self.font) for _ in range(32)]
        self.label_pool_idx = 0
        self.labels_to_draw_queue = []

        # --- ОБНОВЛЕНО: Прогрев FFMPEG в фоновом потоке ---
        def warmup_task():
            # Сохраняем оригинальную функцию запуска процессов
            original_popen = subprocess.Popen

            # Создаем "тихую" версию
            def win_silent_popen(*args, **kwargs):
                if sys.platform == 'win32':
                    # Настройка 1: Скрыть окно через STARTUPINFO
                    startupinfo = subprocess.STARTUPINFO()
                    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
                    startupinfo.wShowWindow = subprocess.SW_HIDE
                    kwargs['startupinfo'] = startupinfo
                    
                    # Настройка 2: Флаг CREATE_NO_WINDOW (самый надежный)
                    kwargs['creationflags'] = 0x08000000 
                return original_popen(*args, **kwargs)

            # Подменяем Popen глобально, но только на секунду прогрева
            subprocess.Popen = win_silent_popen

            try:
                fd, tmp_name = tempfile.mkstemp(suffix=".mp4")
                os.close(fd) 
                
                dummy = np.zeros((16, 16, 3), dtype=np.uint8)
                
                # imageio вызовет наш win_silent_popen вместо обычного
                w = imageio.get_writer(tmp_name, fps=1, format='FFMPEG', macro_block_size=None)
                w.append_data(dummy)
                w.close()
                
                if os.path.exists(tmp_name):
                    os.remove(tmp_name)
            except Exception as e:
                print(f"Background warmup warning: {e}")
            finally:
                # ВАЖНО: Возвращаем оригинальный Popen на место
                subprocess.Popen = original_popen

        threading.Thread(target=warmup_task, daemon=True).start()
    def _init_game_state(self):
        self.running = True
        self.state = "MENU"
        self.project_active = False
        self.mouse_locked = False
        self.set_mouse_lock(False)
        self.unsaved_changes = False
        self.pending_exit_action = None
        self.CHUNK_SIZE = 10
        self.fog_distance = 100
        self.creative_mode = True
        self.tool_mode = 'SELECT'
        self.manipulation_mode = 'MOVE'
        self.edit_mode = False
        self.rect_selecting = False
        self.temp_selection = False
        self.tex_session_active = False       
        self.tex_session_start_states = {}    
        self.local_tex_history = []           
        self.local_tex_history_idx = -1       
        self.current_sky_color = COLOR_SKY
        self.day_time = 0.5
        self.sun_angle_time = 90.0
        self.sun_angle_tilt = 20.0
        self.sun_rotation_y = 0.0 
        self.sun_speed = 0.25
        self.light_dir = np.array([0.0, 1.0, 0.0], dtype=np.float32)
        self.light_color = np.array([1.0, 1.0, 1.0], dtype=np.float32)
        self.ambient_light = np.array([0.2, 0.2, 0.2], dtype=np.float32)
        self.light_intensity = 1.0
        self.fixed_adventure_speed = 5.0
        self.sprint_speed = 10.0
        self.saved_creative_speed = 5.0
        self.crouch_speed = 3
        self.gravity = 20.0
        self.jump_force = 7.0
        self.stand_height = 1.8
        self.crouch_height = 1.2
        self.player_height = 1.8
        self.player_radius = 0.3
        self.vertical_velocity = 0.0
        self.lantern_radius = 15.0
        self.selected_entities = []
        self.selected_faces = {}
        self.highlighted_ent = None
        self.clipboard = []
        self.snap_unit = 0.1
        self.last_paint_settings = {
            'color': [1.0, 1.0, 1.0, 1.0, 0.0, 0.0], 
            'all': True,
            'is_tiling': False,
            'density': 1.0,
            'reflectivity': 0.0, 
            'texture_path': None
        }
        self.last_tex_action_time = 0
        self.last_tex_action_key = None
        self.tex_action_accumulated_states = {} 
        self.default_thickness = 0.1
        self.move_axis = None
        self.transform_axis = 0
        self.vertical_mode = False
        self.constraint_axis = 1
        self.build_start = None
        self.build_normal = None
        self.rect_start = (0, 0)
        self.rect_current = (0, 0)
        self.room_extruding = False
        self.box_extruding = False
        self.strip_extruding = False
        self.strip_points = []
        self.strip_normal = None
        self.strip_plane_p = None
        self.cut_start_point = None
        self.cut_target_ent = None
        self.cut_normal = None
        self.door_tool_state = 'HOVER'
        self.door_animations = []
        self.locked_hinge_edge = -1
        self.temp_hinge_edge = -1
        self.slice_orientation = 0
        self.fps_timer = 0
        self.notification_text = ""
        self.notification_timer = 0
        self.last_manipulation_time = 0
        self.last_click_time = 0
        self.last_action_timestamp = 0
        self.last_x_press = 0
        self.undo_redo_timer = 0
        self.initial_repeat_delay = 400
        self.repeat_interval = 300 
        self.last_slice_pos = None
        self.last_slice_norm = None
        self.last_slice_time = 0
        self.drag_start_pos = None
        self.ent_start_pos = None
        self.drag_snapshot = {}
        self.drag_start_mouse = None
        self.push_pull_active = False
        self.push_pull_ent = None
        self.push_pull_normal = None
        self.push_pull_start_mouse = None
        self.push_pull_original_scale = None
        self.push_pull_original_pos = None
        self.extrusion_start_val = None
    def _init_scene_objects(self):
        self.camera = Camera()
        self.scene = Scene()
        self.color_picker = ColorPicker(self.win_w-320, 100, self.font)
        self.color_picker.update_language(self.tr) # <-- ВАЖНО
        self.file_dialog = FileDialog(self.font)
        self.chunk_meshes = {}
        self.compiled_chunks = set()
        self.chunk_load_queue = []
        self.last_chunk_coord = (None, None, None)
        self.spatial_grid = {}
        self.cached_large_entities = []
        self.large_objects_gl_cache = {}
        self.max_cached_chunks = 20000
        self.force_chunk_update = False
    def find_connected_entities(self, target_ent):
        connected = {target_ent}
        to_process = [target_ent]
        processed = set()
        if target_ent.group_id:
            for ent in self.scene.entities:
                if ent.group_id == target_ent.group_id:
                    if ent not in connected:
                        connected.add(ent)
                        to_process.append(ent)
        candidates = self.scene.entities 
        while to_process:
            current = to_process.pop()
            if current in processed: continue
            processed.add(current)
            min_c, max_c = current.get_aabb()
            margin = 0.015
            min_c -= margin
            max_c += margin
            for other in candidates:
                if other in connected: continue
                min_o, max_o = other.get_aabb()
                if (min_c[0] < max_o[0] and max_c[0] > min_o[0] and
                    min_c[1] < max_o[1] and max_c[1] > min_o[1] and
                    min_c[2] < max_o[2] and max_c[2] > min_o[2]):
                    connected.add(other)
                    to_process.append(other)
        return list(connected)
    def tr(self, key):
        """Helper to get translated string"""
        return TRANSLATIONS.get(self.language, TRANSLATIONS['en']).get(key, key)

    def toggle_language(self):
        self.language = 'ru' if self.language == 'en' else 'en'
        # Пересоздаем UI
        self.create_ui()
        # Обновляем зависимые компоненты
        self.color_picker.refresh_labels()
        if hasattr(self, 'file_dialog'):
            self.file_dialog.refresh_ui_text()
        # Обновляем заголовок окна (опционально)
        title = b"Anterio (RU)" if self.language == 'ru' else b"Anterio"
        sdl2.SDL_SetWindowTitle(self.window, title)
        self.color_picker.update_language(self.tr)
    def _queue_creative_visuals(self):
        px, py, pz = self.camera.pos
        render_dist_sq = 30.0 * 30.0
        for ent in self.scene.entities:
            dx = ent.pos[0] - px
            dy = ent.pos[1] - py
            dz = ent.pos[2] - pz
            dist_sq = dx*dx + dy*dy + dz*dz
            if dist_sq > render_dist_sq and not ent.is_hole:
                continue
            if ent.is_hole:
                min_p, max_p = ent.get_aabb()
                self.line_renderer.add_box(min_p, max_p, color=(1.0, 0.0, 0.0, 0.8))
                p1 = [min_p[0], max_p[1], min_p[2]]; p2 = [max_p[0], max_p[1], max_p[2]]
                p3 = [max_p[0], max_p[1], min_p[2]]; p4 = [min_p[0], max_p[1], max_p[2]]
                self.line_renderer.add_line(p1, p2, (1, 0, 0, 0.8))
                self.line_renderer.add_line(p3, p4, (1, 0, 0, 0.8))
            else:
                for face_idx, c in enumerate(ent.faces_colors):
                    if len(c) > 4 and c[4] > 0.01:
                        min_p, max_p = ent.get_aabb()
                        eps = 0.006 
                        p1, p2, p3, p4 = None, None, None, None
                        if face_idx == 0: 
                            x = max_p[0] + eps
                            p1=[x, min_p[1], max_p[2]]; p2=[x, min_p[1], min_p[2]]
                            p3=[x, max_p[1], min_p[2]]; p4=[x, max_p[1], max_p[2]]
                        elif face_idx == 1: 
                            x = min_p[0] - eps
                            p1=[x, min_p[1], min_p[2]]; p2=[x, min_p[1], max_p[2]]
                            p3=[x, max_p[1], max_p[2]]; p4=[x, max_p[1], min_p[2]]
                        elif face_idx == 2: 
                            y = max_p[1] + eps
                            p1=[min_p[0], y, max_p[2]]; p2=[max_p[0], y, max_p[2]]
                            p3=[max_p[0], y, min_p[2]]; p4=[min_p[0], y, min_p[2]]
                        elif face_idx == 3: 
                            y = min_p[1] - eps
                            p1=[min_p[0], y, min_p[2]]; p2=[max_p[0], y, min_p[2]]
                            p3=[max_p[0], y, max_p[2]]; p4=[min_p[0], y, max_p[2]]
                        elif face_idx == 4: 
                            z = max_p[2] + eps
                            p1=[min_p[0], min_p[1], z]; p2=[max_p[0], min_p[1], z]
                            p3=[max_p[0], max_p[1], z]; p4=[min_p[0], max_p[1], z]
                        elif face_idx == 5: 
                            z = min_p[2] - eps
                            p1=[max_p[0], min_p[1], z]; p2=[min_p[0], min_p[1], z]
                            p3=[min_p[0], max_p[1], z]; p4=[max_p[0], max_p[1], z]
                        if p1:
                            self.sprite_renderer.add_quad(p1, p2, p3, p4, color=(1.0, 0.9, 0.5, 0.8))
    def attempt_merge_selection(self):
        if len(self.selected_entities) < 2: return
        all_changed_entities = []
        any_changes = False
        merged_happened = True
        while merged_happened:
            merged_happened = False
            current_candidates = list(self.selected_entities)
            if len(current_candidates) < 2: break
            for i in range(len(current_candidates)):
                if merged_happened: break
                for j in range(i + 1, len(current_candidates)):
                    ent1 = current_candidates[i]
                    ent2 = current_candidates[j]
                    v1 = ent1.scale[0] * ent1.scale[1] * ent1.scale[2]
                    v2 = ent2.scale[0] * ent2.scale[1] * ent2.scale[2]
                    min1, max1 = ent1.get_aabb()
                    min2, max2 = ent2.get_aabb()
                    bb_min = np.minimum(min1, min2)
                    bb_max = np.maximum(max1, max2)
                    bb_size = bb_max - bb_min
                    if np.any(bb_size < 0.001): continue
                    bb_vol = bb_size[0] * bb_size[1] * bb_size[2]
                    inter_min = np.maximum(min1, min2)
                    inter_max = np.minimum(max1, max2)
                    inter_size = inter_max - inter_min
                    inter_vol = 0.0
                    if np.all(inter_size > 0):
                        inter_vol = inter_size[0] * inter_size[1] * inter_size[2]
                    expected_vol = v1 + v2 - inter_vol
                    if abs(bb_vol - expected_vol) < 0.001:
                        new_center = bb_min + bb_size / 2.0
                        new_ent = Entity(new_center, bb_size, ent1.group_id, None, list(ent1.group_history), copy.deepcopy(ent1.faces_colors))
                        new_ent.faces_tiling = copy.deepcopy(ent1.faces_tiling)
                        new_ent.faces_textures = list(ent1.faces_textures)
                        new_ent.faces_uv_data = copy.deepcopy(ent1.faces_uv_data)
                        new_ent.density = ent1.density
                        new_ent.faces_reflectivity = list(ent1.faces_reflectivity)
                        self.scene.entities.remove(ent1)
                        self.scene.entities.remove(ent2)
                        self.scene.entities.append(new_ent)
                        self.scene.push_transaction(
                            added_ents=[new_ent], 
                            removed_ents=[ent1, ent2], 
                            modified_triplets=[]
                        )
                        self.selected_entities.remove(ent1)
                        self.selected_entities.remove(ent2)
                        self.selected_entities.append(new_ent)
                        if ent1 in self.selected_faces: del self.selected_faces[ent1]
                        if ent2 in self.selected_faces: del self.selected_faces[ent2]
                        all_changed_entities.extend([ent1, ent2, new_ent])
                        merged_happened = True; any_changes = True
                        break 
        if any_changes:
            self.show_notification(self.tr('NOTIF_MERGED'))
            self.mark_scene_changed(changed_entities=all_changed_entities)
    def perform_undo(self):
        changed_list = self.scene.undo()
        if changed_list:
            self.selected_entities = []
            self.selected_faces = {}
            self.mark_scene_changed(changed_entities=changed_list)
            self.show_notification(self.tr('NOTIF_UNDO'))
    def perform_redo(self):
        changed_list = self.scene.redo()
        if changed_list:
            self.selected_entities = []
            self.selected_faces = {}
            self.mark_scene_changed(changed_entities=changed_list)
            self.show_notification(self.tr('NOTIF_REDO'))
    def perform_slice(self, slice_point, slice_normal, target_ent, is_alt=False):
        targets = []
        if is_alt and self.selected_entities:
            targets = list(self.selected_entities)
        elif is_alt:
            targets = self.find_connected_entities(target_ent)
        else:
            if target_ent.group_id is not None:
                targets = [e for e in self.scene.entities if e.group_id == target_ent.group_id]
            else:
                targets = [target_ent]
        axis = np.argmax(np.abs(slice_normal))
        cut_pos = slice_point[axis]
        transaction_added = []
        transaction_removed = []
        visual_updates = []
        for ent in list(targets):
            half = ent.scale[axis] / 2.0
            min_v = ent.pos[axis] - half
            max_v = ent.pos[axis] + half
            if cut_pos <= min_v + 0.001 or cut_pos >= max_v - 0.001:
                continue
            size_1 = cut_pos - min_v
            size_2 = max_v - cut_pos
            scale1 = ent.scale.copy(); scale1[axis] = size_1
            pos1 = ent.pos.copy(); pos1[axis] = min_v + size_1 / 2.0
            scale2 = ent.scale.copy(); scale2[axis] = size_2
            pos2 = ent.pos.copy(); pos2[axis] = cut_pos + size_2 / 2.0
            ent1 = Entity(pos1, scale1, ent.group_id, None, list(ent.group_history), copy.deepcopy(ent.faces_colors))
            ent2 = Entity(pos2, scale2, ent.group_id, None, list(ent.group_history), copy.deepcopy(ent.faces_colors))
            ent1.faces_tiling = copy.deepcopy(ent.faces_tiling)
            ent2.faces_tiling = copy.deepcopy(ent.faces_tiling)
            ent1.faces_textures = list(ent.faces_textures)
            ent2.faces_textures = list(ent.faces_textures)
            ent1.faces_uv_data = copy.deepcopy(ent.faces_uv_data)
            ent2.faces_uv_data = copy.deepcopy(ent.faces_uv_data)
            ent1.density = ent.density
            ent2.density = ent.density
            ent1.faces_reflectivity = list(ent.faces_reflectivity)
            ent2.faces_reflectivity = list(ent.faces_reflectivity)
            TextureUtils.preserve_texture_pos(ent, ent1)
            TextureUtils.preserve_texture_pos(ent, ent2)
            if ent in self.scene.entities:
                self.scene.entities.remove(ent)
            self.scene.entities.append(ent1)
            self.scene.entities.append(ent2)
            transaction_removed.append(ent)
            transaction_added.extend([ent1, ent2])
            if ent in self.selected_entities:
                self.selected_entities.remove(ent)
                self.selected_entities.append(ent1)
                self.selected_entities.append(ent2)
                if ent in self.selected_faces:
                    del self.selected_faces[ent]
            visual_updates.append(ent)
            visual_updates.extend([ent1, ent2])
        if transaction_removed:
            self.last_slice_time = pygame.time.get_ticks()
            self.last_slice_pos = np.array(slice_point, dtype=np.float32)
            self.last_slice_norm = np.array(slice_normal, dtype=np.float32)
            self.scene.push_transaction(
                added_ents=transaction_added,
                removed_ents=transaction_removed,
                modified_triplets=[]
            )
            self.mark_scene_changed(changed_entities=visual_updates)
    def get_face_center_point(self, ent, face_idx):
        center = ent.pos.copy()
        half = ent.scale / 2.0
        if face_idx == 0:   center[0] += half[0]
        elif face_idx == 1: center[0] -= half[0]
        elif face_idx == 2: center[1] += half[1]
        elif face_idx == 3: center[1] -= half[1]
        elif face_idx == 4: center[2] += half[2]
        elif face_idx == 5: center[2] -= half[2]
        return center
    def project_point_to_screen(self, x, y, z):
        aspect = self.draw_w / self.draw_h if self.draw_h > 0 else 1.0
        proj = MatrixUtils.perspective(FOV, aspect, NEAR_CLIP, FAR_CLIP)
        target = self.camera.pos + self.camera.front
        view = MatrixUtils.look_at(self.camera.pos, target, np.array([0,1,0], dtype=np.float32))
        viewport = (0, 0, self.win_w, self.win_h)
        res = MatrixUtils.project(x, y, z, view, proj, viewport)
        if res is None:
            return None
        sx, sy, sz = res
        if sz < 0.0 or sz > 1.0:
            return None
        screen_y = self.win_h - sy
        return int(sx), int(screen_y)
    def process_texture_input(self, dt):
        if not (self.creative_mode and self.color_picker.active and self.selected_entities):
            return
        keys = self.input.get_keys()
        is_ctrl = keys.get(sdl2.SDLK_LCTRL) or keys.get(sdl2.SDLK_RCTRL)
        is_shift = keys.get(sdl2.SDLK_LSHIFT) or keys.get(sdl2.SDLK_RSHIFT)
        move_step = (0.01 if is_ctrl else 0.1) * 3.0 * dt 
        scale_step = (0.01 if is_ctrl else 0.1) * 3.0 * dt 
        action_key = None
        d_off = [0.0, 0.0]
        d_scl_factor = [1.0, 1.0]
        if keys.get(sdl2.SDLK_w): d_off[1] += move_step; action_key = 'MOVE_Y_POS'
        if keys.get(sdl2.SDLK_s): d_off[1] -= move_step; action_key = 'MOVE_Y_NEG'
        if keys.get(sdl2.SDLK_d): d_off[0] += move_step; action_key = 'MOVE_X_POS'
        if keys.get(sdl2.SDLK_a): d_off[0] -= move_step; action_key = 'MOVE_X_NEG'
        factor_zoom_in = 1.0 - scale_step
        factor_zoom_out = 1.0 + scale_step
        f_up_right  = factor_zoom_out if is_shift else factor_zoom_in
        f_down_left = factor_zoom_in if is_shift else factor_zoom_out
        if keys.get(sdl2.SDLK_UP):    d_scl_factor[1] *= f_up_right;   action_key = 'SCALE_Y_UP'
        if keys.get(sdl2.SDLK_DOWN):  d_scl_factor[1] *= f_down_left;  action_key = 'SCALE_Y_DOWN'
        if keys.get(sdl2.SDLK_RIGHT): d_scl_factor[0] *= f_up_right;   action_key = 'SCALE_X_RIGHT'
        if keys.get(sdl2.SDLK_LEFT):  d_scl_factor[0] *= f_down_left;  action_key = 'SCALE_X_LEFT'
        if not is_shift and (d_scl_factor[0] != 1.0 or d_scl_factor[1] != 1.0):
            if d_scl_factor[1] != 1.0: 
                d_scl_factor[0] = d_scl_factor[1]
                action_key = 'SCALE_UNIFORM_' + ('A' if d_scl_factor[1] < 1.0 else 'B')
            elif d_scl_factor[0] != 1.0: 
                d_scl_factor[1] = d_scl_factor[0]
                action_key = 'SCALE_UNIFORM_' + ('A' if d_scl_factor[0] < 1.0 else 'B')
        if action_key:
            for ent in self.selected_entities:
                faces_to_edit = range(6)
                if not self.color_picker.paint_all and ent in self.selected_faces:
                    faces_to_edit = self.selected_faces[ent]
                new_uv_data = copy.deepcopy(ent.faces_uv_data)
                for f_idx in faces_to_edit:
                    data = new_uv_data[f_idx]
                    local_move_x = d_off[0] * (-1 if data['fliph'] else 1)
                    local_move_y = d_off[1] * (-1 if data['flipv'] else 1)
                    data['off'][0] += local_move_x
                    data['off'][1] += local_move_y
                    curr_scl = list(d_scl_factor)
                    if data['rot'] % 2 == 1:
                        curr_scl[0], curr_scl[1] = curr_scl[1], curr_scl[0]
                    data['scl'][0] *= curr_scl[0]
                    data['scl'][1] *= curr_scl[1]
                    data['scl'][0] = max(0.001, min(1000.0, data['scl'][0]))
                    data['scl'][1] = max(0.001, min(1000.0, data['scl'][1]))
                ent.faces_uv_data = new_uv_data
                self.invalidate_entity_chunks(ent)
            self.force_chunk_update = True
            current_time = pygame.time.get_ticks()
            if (self.last_tex_action_key != action_key) or (current_time - self.last_tex_action_time > 500):
                current_state = self._get_current_local_state()
                if self.local_tex_history_idx < len(self.local_tex_history) - 1:
                    self.local_tex_history = self.local_tex_history[:self.local_tex_history_idx+1]
                self.local_tex_history.append(current_state)
                self.local_tex_history_idx += 1
            else:
                current_state = self._get_current_local_state()
                if self.local_tex_history_idx >= 0:
                    self.local_tex_history[self.local_tex_history_idx] = current_state
            self.last_tex_action_time = current_time
            self.last_tex_action_key = action_key
        else:
            if pygame.time.get_ticks() - self.last_tex_action_time > 500:
                self.last_tex_action_key = None
    def compile_large_entities(self):
        current_uids = {ent.uid for ent in self.cached_large_entities}
        cached_uids = list(self.large_objects_gl_cache.keys())
        for uid in cached_uids:
            if uid not in current_uids:
                # Очистка старых мешей
                mesh_dict = self.large_objects_gl_cache[uid]
                for mesh in mesh_dict.values():
                    mesh.delete()
                del self.large_objects_gl_cache[uid]
                
        for ent in self.cached_large_entities:
            if ent.uid in self.large_objects_gl_cache:
                continue
            batches = ChunkMeshBuilder.build_chunk_data([ent], (0, 0, 0), self.texture_manager)
            mesh_dict = {}
            # Исправлено распаковывание ключа
            for (tex_id, mode, is_trans), data_array in batches.items():
                mesh_dict[(tex_id, mode, is_trans)] = MeshBuffer(data_array)
            self.large_objects_gl_cache[ent.uid] = mesh_dict
    def draw_measurements(self, box_min, box_max, cursor_point, show_components=True):
        if not self.mouse_locked:
            return
        if self.rect_selecting or self.color_picker.active:
            return
        if show_components:
            def draw_axis_full(axis_idx, line_color, text_color, label_prefix):
                total_len = abs(box_max[axis_idx] - box_min[axis_idx])
                if total_len < 0.001: return
                p_min_proj = cursor_point.copy()
                p_min_proj[axis_idx] = box_min[axis_idx]
                p_max_proj = cursor_point.copy()
                p_max_proj[axis_idx] = box_max[axis_idx]
                self.line_renderer.add_line(p_min_proj, p_max_proj, line_color)
                val_min = box_min[axis_idx]
                val_max = box_max[axis_idx]
                val_cursor = cursor_point[axis_idx]
                clamped_cursor_val = max(min(val_min, val_max), min(max(val_min, val_max), val_cursor))
                p_clamped_cursor = cursor_point.copy()
                p_clamped_cursor[axis_idx] = clamped_cursor_val
                d1 = abs(clamped_cursor_val - val_min)
                d2 = total_len - d1 
                s_start = self.project_point_to_screen(*p_min_proj)
                s_end = self.project_point_to_screen(*p_max_proj)
                final_offset = (0, -20)
                if s_start and s_end:
                    dx = s_end[0] - s_start[0]
                    dy = s_end[1] - s_start[1]
                    is_horizontal = abs(dx) > abs(dy)
                    offset_px = 30
                    if is_horizontal: final_offset = (0, -offset_px)
                    else:             final_offset = (offset_px, 0)
                if d1 > 0.01:
                    mid1 = (p_min_proj + p_clamped_cursor) / 2.0
                    val1 = f"{d1:.2f}"
                    if d2 < 0.01: val1 = f"{label_prefix}: {d1:.2f}"
                    self.queue_label_at(mid1, val1, text_color, final_offset)
                if d2 > 0.01:
                    mid2 = (p_clamped_cursor + p_max_proj) / 2.0
                    val2 = f"{d2:.2f}"
                    if d1 < 0.01: val2 = f"{label_prefix}: {d2:.2f}"
                    self.queue_label_at(mid2, val2, text_color, final_offset)
            draw_axis_full(0, (1, 0.2, 0.2, 1), (1.0, 0.75, 0.75), "X")
            draw_axis_full(1, (0.2, 1, 0.2, 1), (0.75, 1.0, 0.75), "Y")
            draw_axis_full(2, (0.4, 0.4, 1, 1), (0.75, 0.75, 1.0), "Z")
        else:
            dist = np.linalg.norm(box_max - box_min)
            self.line_renderer.add_line(box_min, box_max, (1, 1, 0, 0.8))
            mid = (box_min + box_max) / 2.0
            self.queue_label_at(mid, f"L: {dist:.2f}", (1.0, 1.0, 0.8), (20, -20))
    def queue_label_at(self, pos_3d, text, color, offset=(0,0)):
        scr = self.project_point_to_screen(pos_3d[0], pos_3d[1], pos_3d[2])
        if scr:
            if self.label_pool_idx >= len(self.label_pool):
                return
            lbl = self.label_pool[self.label_pool_idx]
            self.label_pool_idx += 1
            r, g, b = color
            col_int = (int(r * 255), int(g * 255), int(b * 255))
            if lbl.color != col_int:
                lbl.current_text = None
            lbl.color = col_int
            lbl.set_text(text)
            tx = scr[0] + offset[0]
            ty = scr[1] + offset[1]
            if offset[0] < 0: tx -= lbl.w
            if offset[1] < 0: ty -= lbl.h
            self.labels_to_draw_queue.append((lbl, tx, ty))
    def create_box_by_2_points(self, p1, p2):
        p_min = np.minimum(p1, p2)
        p_max = np.maximum(p1, p2)
        size = p_max - p_min
        center = (p_min + p_max) / 2.0
        new_ent = Entity(center, size) 
        c = self.last_paint_settings['color']
        new_ent.faces_colors = [list(c)] * 6
        is_tiling_val = self.last_paint_settings.get('is_tiling', False)
        new_ent.faces_tiling = [is_tiling_val] * 6
        new_ent.density = self.last_paint_settings.get('density', 1.0)
        refl_val = self.last_paint_settings.get('reflectivity', 0.0)
        new_ent.faces_reflectivity = [refl_val] * 6
        tex = self.last_paint_settings.get('texture_path', None)
        if tex:
            self.texture_manager.load_from_file(tex) 
            new_ent.faces_textures = [tex] * 6
        self.scene.add_entity(new_ent)
        self.mark_scene_changed(changed_entities=[new_ent])
    def create_room_by_2_points(self, p1, p2):
        p_min = np.minimum(p1, p2)
        p_max = np.maximum(p1, p2)
        size = p_max - p_min
        center = (p_min + p_max) / 2.0
        center, size = snap_bounds_to_grid_3d(center, size, precision=0.01)
        self._build_room_geometry(center, size, color=self.last_paint_settings['color'])
    def get_closest_edge_info(self, ent, hit_point):
        half = ent.scale / 2.0
        corners_signs = [
            [-1, 1, 1], [1, 1, 1], [1, -1, 1], [-1, -1, 1],
            [-1, 1, -1], [1, 1, -1], [1, -1, -1], [-1, -1, -1]
        ]
        world_corners = [ent.pos + np.array(c) * half for c in corners_signs]
        edges_indices = [
            (0, 1), (1, 2), (2, 3), (3, 0), (4, 5), (5, 6), (6, 7), (7, 4), 
            (0, 4), (1, 5), (2, 6), (3, 7)
        ]
        best_dist = float('inf')
        best_idx = -1
        for i, (s_idx, e_idx) in enumerate(edges_indices):
            p1, p2 = world_corners[s_idx], world_corners[e_idx]
            line_vec = p2 - p1
            point_vec = hit_point - p1
            line_len = np.linalg.norm(line_vec)
            if line_len < 1e-6: continue
            line_unit = line_vec / line_len
            proj = np.dot(point_vec, line_unit)
            if proj < 0: closest = p1
            elif proj > line_len: closest = p2
            else: closest = p1 + line_unit * proj
            dist = np.linalg.norm(hit_point - closest)
            if dist < best_dist:
                best_dist = dist
                best_idx = i
        if best_idx != -1:
            s, e = edges_indices[best_idx]
            pivot = (world_corners[s] + world_corners[e]) / 2.0
            axis = (world_corners[e] - world_corners[s])
            axis = axis / np.linalg.norm(axis)
            return best_idx, pivot, axis
        return -1, ent.pos, np.array([0,1,0])
    def trigger_door_animation(self, ent):
        targets = [ent]
        master_ent = ent
        if ent.group_id:
            group_members = [e for e in self.scene.entities if e.group_id == ent.group_id]
            hinge_owners = [e for e in group_members if e.hinge_edge != -1]
            if not hinge_owners: return 
            master_ent = hinge_owners[0]
            targets = group_members
        else:
            if ent.hinge_edge == -1: return
        if any(t.is_animating for t in targets): return
        idx = master_ent.hinge_edge
        half = master_ent.scale / 2.0
        corners_signs = [[-1, 1, 1], [1, 1, 1], [1, -1, 1], [-1, -1, 1], [-1, 1, -1], [1, 1, -1], [1, -1, -1], [-1, -1, -1]]
        edges_indices = [(0, 1), (1, 2), (2, 3), (3, 0), (4, 5), (5, 6), (6, 7), (7, 4), (0, 4), (1, 5), (2, 6), (3, 7)]
        s, e = edges_indices[idx]
        wc = [master_ent.pos + np.array(c) * half for c in corners_signs]
        pivot = (wc[s] + wc[e]) / 2.0
        axis = (wc[e] - wc[s])
        norm_val = np.linalg.norm(axis)
        if norm_val < 1e-6: axis = np.array([0.0, 1.0, 0.0])
        else: axis = axis / norm_val
        dom_axis = np.argmax(np.abs(axis))
        if axis[dom_axis] < 0:
            axis = -axis
        target_delta = 90.0 if not master_ent.door_open else -90.0
        dim_max = max(master_ent.scale)
        duration = 0.07 + (dim_max * 0.1) 
        speed = target_delta / duration 
        chunks_to_rebuild = set()
        for target in targets:
            target.is_animating = True 
            if target.uid in self.large_objects_gl_cache:
                mb_solid, mb_trans = self.large_objects_gl_cache[target.uid]
                if mb_solid: mb_solid.delete()
                if mb_trans: mb_trans.delete()
                del self.large_objects_gl_cache[target.uid]
            half = target.scale / 2.0
            mn = target.pos - half
            mx = target.pos + half
            scx, scy, scz = self.get_chunk_coords(mn[0], mn[2], mn[1])
            ecx, ecy, ecz = self.get_chunk_coords(mx[0], mx[2], mx[1])
            for cx in range(scx - 1, ecx + 2):
                for cy in range(scy - 1, ecy + 2):
                    for cz in range(scz - 1, ecz + 2):
                        chunks_to_rebuild.add((cx, cy, cz))
            self.door_animations.append({
                'ent': target, 'master': master_ent, 'pivot': pivot, 'axis': axis,
                'current_angle': 0.0, 'target_delta': target_delta, 'speed': speed,
                'original_pos': target.pos.copy(), 'original_scale': target.scale.copy(),
                'is_opening': not master_ent.door_open
            })
        for (cx, cy, cz) in chunks_to_rebuild:
            self.compile_single_chunk(cx, cy, cz)
        self.scene_dirty_creative = True
    def _generate_lit_door_geometry(self):
        batches = {}
        white_tex_id = self.texture_manager.get_white_texture()
        base_normals = [
            np.array([ 1,  0,  0], dtype=np.float32), 
            np.array([-1,  0,  0], dtype=np.float32), 
            np.array([ 0,  1,  0], dtype=np.float32), 
            np.array([ 0, -1,  0], dtype=np.float32), 
            np.array([ 0,  0,  1], dtype=np.float32), 
            np.array([ 0,  0, -1], dtype=np.float32), 
        ]
        raw_uvs_base = [
            np.array([0.0, 0.0]), np.array([1.0, 0.0]),
            np.array([1.0, 1.0]), np.array([0.0, 1.0])
        ]
        for anim in self.door_animations:
            ent = anim['ent']
            pos = anim['original_pos']
            uid_val = int(ent.uid[:4], 16) if ent.uid else 0
            noise = (uid_val % 100) * 0.000005 
            major_expand = 0.001 + noise 
            minor_expand = 0.00005 + (noise * 0.1)
            s = anim['original_scale']
            min_dim_idx = np.argmin(s)
            final_scale = np.array(s, copy=True)
            for i in range(3):
                if i == min_dim_idx: final_scale[i] += major_expand
                else: final_scale[i] += minor_expand
            scale = final_scale
            pivot = anim['pivot']
            angle_deg = anim['current_angle']
            axis = anim['axis']
            rad = math.radians(angle_deg)
            c = math.cos(rad); si = math.sin(rad)
            ux, uy, uz = axis
            rot_mat = np.array([
                [c + ux**2*(1-c),    ux*uy*(1-c) - uz*si, ux*uz*(1-c) + uy*si],
                [uy*ux*(1-c) + uz*si, c + uy**2*(1-c),    uy*uz*(1-c) - ux*si],
                [uz*ux*(1-c) - uy*si, uz*uy*(1-c) + ux*si, c + uz**2*(1-c)]
            ], dtype=np.float32)
            rotated_normals = [np.dot(rot_mat, n) for n in base_normals]
            dx, dy, dz = scale / 2.0
            cx, cy, cz = pos
            corners_orig = [
                np.array([cx-dx, cy-dy, cz+dz]), np.array([cx+dx, cy-dy, cz+dz]),
                np.array([cx+dx, cy+dy, cz+dz]), np.array([cx-dx, cy+dy, cz+dz]),
                np.array([cx-dx, cy-dy, cz-dz]), np.array([cx+dx, cy-dy, cz-dz]),
                np.array([cx+dx, cy+dy, cz-dz]), np.array([cx-dx, cy+dy, cz-dz])
            ]
            c_v = []
            for p in corners_orig:
                c_v.append(pivot + np.dot(rot_mat, (p - pivot)))
            faces_indices = [
                ([1, 5, 6, 2], 0), ([4, 0, 3, 7], 1), ([3, 2, 6, 7], 2),
                ([4, 5, 1, 0], 3), ([0, 1, 2, 3], 4), ([5, 4, 7, 6], 5)
            ]
            for indices, f_idx in faces_indices:
                col_data = ent.faces_colors[f_idx] 
                r, g, b = col_data[0], col_data[1], col_data[2]
                a = col_data[3] if len(col_data) > 3 else 1.0
                emit = col_data[4] if len(col_data) > 4 else 0.0
                gloss = col_data[5] if len(col_data) > 5 else 0.0
                reflect = ent.faces_reflectivity[f_idx] if hasattr(ent, 'faces_reflectivity') else 0.0 
                tex_path = ent.faces_textures[f_idx]
                target_tex_id = white_tex_id
                target_mode = 0
                if tex_path:
                    found = self.texture_manager.load_from_file(tex_path)
                    if found is not None:
                        target_tex_id = found
                        target_mode = 2 if ent.faces_tiling[f_idx] else 1
                batch_key = (target_tex_id, target_mode)
                if batch_key not in batches: batches[batch_key] = []
                target_list = batches[batch_key]
                face_aspect = 1.0
                if f_idx in [0, 1]: 
                    if scale[1] > 0.001: face_aspect = scale[2] / scale[1]
                elif f_idx in [2, 3]: 
                    if scale[2] > 0.001: face_aspect = scale[0] / scale[2]
                elif f_idx in [4, 5]: 
                    if scale[1] > 0.001: face_aspect = scale[0] / scale[1]
                final_uvs = []
                if tex_path:
                    uv_data = ent.faces_uv_data[f_idx]
                    off_x, off_y = uv_data['off']
                    scl_x, scl_y = uv_data['scl']
                    rot_uv = uv_data['rot']
                    flip_h = uv_data['fliph']
                    flip_v = uv_data['flipv']
                    if rot_uv % 2 != 0: scl_x, scl_y = scl_y, scl_x
                    for uv in raw_uvs_base:
                        curr = uv - 0.5
                        curr[0] -= off_x; curr[1] -= off_y
                        if abs(scl_x) > 0.0001: curr[0] /= scl_x
                        if abs(scl_y) > 0.0001: curr[1] /= scl_y
                        if flip_h: curr[0] = -curr[0]
                        if flip_v: curr[1] = -curr[1]
                        curr[0] *= face_aspect
                        if rot_uv == 1:   curr = np.array([-curr[1], curr[0]])
                        elif rot_uv == 2: curr = np.array([-curr[0], -curr[1]])
                        elif rot_uv == 3: curr = np.array([curr[1], -curr[0]])
                        if face_aspect > 0.0001: curr[0] /= face_aspect
                        curr += 0.5
                        final_uvs.append(curr)
                else:
                    sx, sy, sz = scale
                    noise_density = 0.03
                    u_len, v_len = 1.0, 1.0
                    if f_idx in [0, 1]: 
                        u_len = sz * noise_density
                        v_len = sy * noise_density
                    elif f_idx in [2, 3]: 
                        u_len = sx * noise_density
                        v_len = sz * noise_density
                    elif f_idx in [4, 5]: 
                        u_len = sx * noise_density
                        v_len = sy * noise_density
                    final_uvs.append(np.array([0.0, 0.0]))
                    final_uvs.append(np.array([u_len, 0.0]))
                    final_uvs.append(np.array([u_len, v_len]))
                    final_uvs.append(np.array([0.0, v_len]))
                nx, ny, nz = rotated_normals[f_idx]
                p0, p1, p2, p3 = c_v[indices[0]], c_v[indices[1]], c_v[indices[2]], c_v[indices[3]]
                u1, v1 = final_uvs[0]; u2, v2 = final_uvs[1]
                u3, v3 = final_uvs[2]; u4, v4 = final_uvs[3]
                target_list.extend([p0[0], p0[1], p0[2], r, g, b, a, nx, ny, nz, u1, v1, emit, gloss, reflect])
                target_list.extend([p1[0], p1[1], p1[2], r, g, b, a, nx, ny, nz, u2, v2, emit, gloss, reflect])
                target_list.extend([p2[0], p2[1], p2[2], r, g, b, a, nx, ny, nz, u3, v3, emit, gloss, reflect])
                target_list.extend([p0[0], p0[1], p0[2], r, g, b, a, nx, ny, nz, u1, v1, emit, gloss, reflect])
                target_list.extend([p2[0], p2[1], p2[2], r, g, b, a, nx, ny, nz, u3, v3, emit, gloss, reflect])
                target_list.extend([p3[0], p3[1], p3[2], r, g, b, a, nx, ny, nz, u4, v4, emit, gloss, reflect]) 
        final_batches = {}
        for k, v in batches.items():
            final_batches[k] = np.array(v, dtype=np.float32)
        return final_batches
    def _get_surface_height(self, x, z):
        max_h = -float('inf')
        is_hole_here = False
        for ent in self.scene.entities:
            if ent.density < 0.7: continue
            if ent.is_hole:
                half = ent.scale / 2.0
                margin = 0.05 
                if (x > ent.pos[0] - half[0] + margin and x < ent.pos[0] + half[0] - margin and
                    z > ent.pos[2] - half[2] + margin and z < ent.pos[2] + half[2] - margin):
                    is_hole_here = True
                    break
        if not is_hole_here:
            max_h = 0.0
        for ent in self.scene.entities:
            if ent.is_hole or ent.is_animating: continue
            if ent.density < 0.5: continue
            half = ent.scale / 2.0
            if (x >= ent.pos[0] - half[0] and x <= ent.pos[0] + half[0] and
                z >= ent.pos[2] - half[2] and z <= ent.pos[2] + half[2]):
                top = ent.pos[1] + half[1]
                if top > max_h:
                    max_h = top
        return max_h
    def update_door_animations(self, dt):
        finished = []
        for anim in self.door_animations:
            step = anim['speed'] * dt
            anim['current_angle'] += step
            finished_step = False
            if anim['target_delta'] > 0:
                if anim['current_angle'] >= anim['target_delta']:
                    anim['current_angle'] = anim['target_delta']
                    finished_step = True
            else:
                if anim['current_angle'] <= anim['target_delta']:
                    anim['current_angle'] = anim['target_delta']
                    finished_step = True
            if finished_step:
                finished.append(anim)
        chunks_to_invalidate = set()
        for anim in finished:
            self.door_animations.remove(anim)
            ent = anim['ent']
            master = anim['master']
            ent.is_animating = False
            pivot = anim['pivot']
            axis_vec = anim['axis']
            rotation_angle = anim['target_delta']
            axis_idx = np.argmax(np.abs(axis_vec))
            def collect_chunks(pos, scale, target_set):
                half = scale / 2.0
                mn = pos - half
                mx = pos + half
                scx, scy, scz = self.get_chunk_coords(mn[0], mn[2], mn[1])
                ecx, ecy, ecz = self.get_chunk_coords(mx[0], mx[2], mx[1])
                for cx in range(scx, ecx + 1):
                    for cy in range(scy, ecy + 1):
                        for cz in range(scz, ecz + 1):
                            target_set.add((cx, cy, cz))
            collect_chunks(anim['original_pos'], anim['original_scale'], chunks_to_invalidate)
            rel_pos = anim['original_pos'] - pivot
            new_rel = np.copy(rel_pos)
            new_scale = np.copy(anim['original_scale'])
            is_positive = (rotation_angle > 0)
            if axis_idx == 1:
                if is_positive: new_rel[0] = rel_pos[2]; new_rel[2] = -rel_pos[0]
                else:           new_rel[0] = -rel_pos[2]; new_rel[2] = rel_pos[0]
                new_scale[0] = anim['original_scale'][2]
                new_scale[2] = anim['original_scale'][0]
            elif axis_idx == 0:
                if is_positive: new_rel[1] = -rel_pos[2]; new_rel[2] = rel_pos[1]
                else:           new_rel[1] = rel_pos[2]; new_rel[2] = -rel_pos[1]
                new_scale[1] = anim['original_scale'][2]
                new_scale[2] = anim['original_scale'][1]
            elif axis_idx == 2:
                if is_positive: new_rel[0] = -rel_pos[1]; new_rel[1] = rel_pos[0]
                else:           new_rel[0] = rel_pos[1]; new_rel[1] = -rel_pos[0]
                new_scale[0] = anim['original_scale'][1]
                new_scale[1] = anim['original_scale'][0]
            ent.pos = pivot + new_rel
            ent.scale = new_scale
            ent.pos, ent.scale = snap_bounds_to_grid_3d(ent.pos, ent.scale, precision=0.01)
            rot_dir = 1 if rotation_angle > 0 else -1
            if axis_idx == 1: TextureUtils.rotate_entity_data(ent, 1, rot_dir)
            elif axis_idx == 0: TextureUtils.rotate_entity_data(ent, 0, rot_dir)
            elif axis_idx == 2: TextureUtils.rotate_entity_data(ent, 2, rot_dir)
            ent.door_angle = 0.0
            ent.door_open = not ent.door_open
            if ent == master:
                new_hinge_idx, _, _ = self.get_closest_edge_info(ent, pivot)
                if new_hinge_idx != -1:
                    ent.hinge_edge = new_hinge_idx
            collect_chunks(ent.pos, ent.scale, chunks_to_invalidate)
        if finished:
            self.build_spatial_grid()
            for (cx, cy, cz) in chunks_to_invalidate:
                self.invalidate_chunk(cx, cy, cz)
            self.force_chunk_update = True
            self.unsaved_changes = True
            self.cached_large_entities = [e for e in self.scene.entities if max(e.scale) > self.CHUNK_SIZE]
    def get_chunk_coords(self, x, z, y=None):
        val_y = y if y is not None else 0
        cx = int(math.floor(x / self.CHUNK_SIZE))
        cy = int(math.floor(val_y / self.CHUNK_SIZE))
        cz = int(math.floor(z / self.CHUNK_SIZE))
        return cx, cy, cz
    def build_spatial_grid(self):
        self.spatial_grid = {}
        for ent in self.scene.entities:
            half = ent.scale / 2.0
            e_min = ent.pos - half
            e_max = ent.pos + half
            scx, scy, scz = self.get_chunk_coords(e_min[0], e_min[2], e_min[1])
            ecx, ecy, ecz = self.get_chunk_coords(e_max[0], e_max[2], e_max[1])
            for cx in range(scx, ecx + 1):
                for cy in range(scy, ecy + 1):
                    for cz in range(scz, ecz + 1):
                        key = (cx, cy, cz)
                        if key not in self.spatial_grid:
                            self.spatial_grid[key] = []
                        self.spatial_grid[key].append(ent)
    def get_candidates_for_ray(self, ray_o, ray_d, max_dist=100.0):
        candidates = set()
        step_size = 2.0 
        current_dist = 0.0
        limit = min(max_dist, FAR_CLIP)
        while current_dist < limit:
            p = ray_o + ray_d * current_dist
            cx, cy, cz = self.get_chunk_coords(p[0], p[2], p[1])
            key = (cx, cy, cz)
            if key in self.spatial_grid:
                candidates.update(self.spatial_grid[key])
            current_dist += step_size
        return list(candidates)
    def get_nearby_entities(self, px, pz, radius=1, py=None):
        if py is None:
            py = self.camera.pos[1]
        cx, cy, cz = self.get_chunk_coords(px, pz, py)
        nearby = []
        for dx in range(-radius, radius + 1):
            for dy in range(-radius, radius + 1):
                for dz in range(-radius, radius + 1):
                    key = (cx + dx, cy + dy, cz + dz)
                    if key in self.spatial_grid:
                        nearby.extend(self.spatial_grid[key])
        return nearby
    def calculate_extrusion_raw(self, ray_o, ray_d, base_rect_or_p, normal_override=None):
        if isinstance(base_rect_or_p, dict):
            p1 = base_rect_or_p['p1']
            p2 = base_rect_or_p['p2']
            base_center = (p1 + p2) / 2.0
        else:
            base_center = base_rect_or_p
        if normal_override is not None:
            norm = normal_override
        elif self.tool_mode == 'STRIP':
            norm = self.strip_normal
        else:
            norm = np.zeros(3)
            norm[self.constraint_axis] = 1.0
        axis_idx = np.argmax(np.abs(norm))
        axis_vec = np.zeros(3)
        axis_vec[axis_idx] = 1.0
        w0 = ray_o - base_center
        a = np.dot(ray_d, ray_d)       
        b = np.dot(ray_d, axis_vec)
        c = np.dot(axis_vec, axis_vec) 
        d = np.dot(ray_d, w0)
        e = np.dot(axis_vec, w0)
        denom = a * c - b * b
        if denom < 1e-5:
            return 0.0
        s = (a * e - b * d) / denom
        return s
    def open_color_picker(self):
        self.temp_selection = False 
        if not self.selected_entities:
            if self.auto_select_hovered():
                self.temp_selection = True
        for ent in self.selected_entities:
            if ent.is_hole:
                self.show_notification(self.tr('NOTIF_NO_PAINT_HOLES'))
                # Сбрасываем временное выделение, если оно было
                if self.temp_selection:
                    self.selected_entities = []
                    self.selected_faces = {}
                    self.temp_selection = False
                return
        if self.selected_entities:
            self.tex_session_start_states = {e.uid: e.to_dict() for e in self.selected_entities}
            current_state = self._get_current_local_state()
            self.local_tex_history = [current_state]
            self.local_tex_history_idx = 0
            self.tex_session_active = True
            target_ent = self.selected_entities[-1]
            face_idx = 2 
            if target_ent in self.selected_faces and self.selected_faces[target_ent]:
                face_idx = list(self.selected_faces[target_ent])[-1]
                self.color_picker.paint_all = False 
            else:
                self.color_picker.paint_all = True 
            c = target_ent.faces_colors[face_idx]
            r, g, b = c[0], c[1], c[2]
            a = c[3] if len(c) > 3 else 1.0
            e = c[4] if len(c) > 4 else 0.0
            gloss = c[5] if len(c) > 5 else 0.0 
            is_tiling = target_ent.faces_tiling[face_idx]
            dens = target_ent.density
            refl = target_ent.faces_reflectivity[face_idx]
            tex_path = target_ent.faces_textures[face_idx]
            self.color_picker.set_full_data(r, g, b, a, e, gloss, tex_path, is_tiling, dens, refl)
        self.color_picker.active = True
        self.color_picker.rect.x = self.win_w - 320
        self.mouse_locked = False
        self.set_mouse_lock(False)
    def open_texture_dialog(self):
        self.file_dialog.open('load', self.on_texture_selected, extensions=['.png', '.jpg', '.jpeg', '.bmp', '.gif'])
    def on_texture_selected(self, filepath):
        if not filepath: return
        tex_id = self.texture_manager.load_from_file(filepath)
        if tex_id is None:
            self.show_notification(self.tr('ERR_TEX_LOAD'))
            return
        tex_w = self.texture_manager.textures[os.path.abspath(filepath)]['w']
        tex_h = self.texture_manager.textures[os.path.abspath(filepath)]['h']
        img_aspect = tex_w / tex_h if tex_h > 0 else 1.0
        if self.selected_entities:
            states_before = {e.uid: e.to_dict() for e in self.selected_entities}
            for ent in self.selected_entities:
                faces_to_paint = []
                if self.color_picker.paint_all: faces_to_paint = range(6)
                elif ent in self.selected_faces: faces_to_paint = self.selected_faces[ent]
                new_textures = list(ent.faces_textures)
                new_uv_data = copy.deepcopy(ent.faces_uv_data)
                sx, sy, sz = ent.scale
                face_dims = [(sz, sy), (sz, sy), (sx, sz), (sx, sz), (sx, sy), (sx, sy)]
                for f_idx in faces_to_paint:
                    new_textures[f_idx] = filepath
                    wall_w, wall_h = face_dims[f_idx]
                    wall_aspect = wall_w / wall_h if wall_h > 0 else 1.0
                    s_u, s_v = 1.0, 1.0
                    if wall_aspect > img_aspect: 
                        ratio = wall_aspect / img_aspect
                        if ratio > 1.0: s_u = 1.0 / ratio
                    else: 
                        ratio = img_aspect / wall_aspect
                        if ratio > 1.0: s_v = 1.0 / ratio
                    new_uv_data[f_idx] = {'off': [0.0, 0.0], 'scl': [s_u, s_v], 'rot': 0, 'fliph': 0, 'flipv': 0}
                ent.faces_textures = new_textures
                ent.faces_uv_data = new_uv_data
            new_state = self._get_current_local_state()
            if self.local_tex_history_idx < len(self.local_tex_history) - 1:
                self.local_tex_history = self.local_tex_history[:self.local_tex_history_idx+1]
            self.local_tex_history.append(new_state)
            self.local_tex_history_idx += 1
            self.color_picker.set_texture_name(filepath)
            states_after = {e.uid: e.to_dict() for e in self.selected_entities}
            self.scene.push_modification(states_before, states_after)
            self.mark_scene_changed(changed_entities=self.selected_entities)
            self.show_notification(self.tr('NOTIF_TEX_APPLIED'))
    def get_entities_in_chunk(self, cx, cy, cz):
        return self.spatial_grid.get((cx, cy, cz), [])
    def get_visible_large_entities(self, radius_sq):
        px, py, pz = self.camera.pos
        visible = []
        view_dist_sq = (math.sqrt(radius_sq) * self.CHUNK_SIZE + 4.0) ** 2
        for ent in self.cached_large_entities:
            if ent.is_hole: continue 
            half = ent.scale / 2.0
            min_p = ent.pos - half
            max_p = ent.pos + half
            dist_sq = 0.0
            if px < min_p[0]: dist_sq += (min_p[0] - px)**2
            elif px > max_p[0]: dist_sq += (px - max_p[0])**2
            if py < min_p[1]: dist_sq += (min_p[1] - py)**2
            elif py > max_p[1]: dist_sq += (py - max_p[1])**2
            if pz < min_p[2]: dist_sq += (min_p[2] - pz)**2
            elif pz > max_p[2]: dist_sq += (pz - max_p[2])**2
            if dist_sq < view_dist_sq:
                visible.append(ent)
        return visible
    def compile_single_chunk(self, cx, cy, cz):
        self.invalidate_chunk(cx, cy, cz)
        ents = self.get_entities_in_chunk(cx, cy, cz)
        if not ents:
            self.compiled_chunks.add((cx, cy, cz))
            return 
        batches = ChunkMeshBuilder.build_chunk_data(ents, (cx, cy, cz), self.texture_manager)
        chunk_meshes_dict = {}
        # Исправлено распаковывание ключа: добавлено is_trans
        for (tex_id, mode, is_trans), data_array in batches.items():
            chunk_meshes_dict[(tex_id, mode, is_trans)] = MeshBuffer(data_array)
        if chunk_meshes_dict:
            self.chunk_meshes[(cx, cy, cz)] = chunk_meshes_dict
        self.compiled_chunks.add((cx, cy, cz))
    def render_video_sequence(self, filename):
        if not imageio:
            self.show_notification("ERROR: imageio library not found")
            return

        path = self.cine_cam.get_active_path()
        if len(path.keyframes) < 2:
            self.show_notification("Need at least 2 keyframes!")
            return

        if hasattr(self, 'file_dialog'):
            self.file_dialog.active = False

        # Параметры path.is_looped и path.loop_duration уже обновлены через меню
        
        total_duration = path.get_total_duration()
        fps = 60
        total_frames = int(total_duration * fps)
        
        print(f"Starting render: {filename}, {total_frames} frames, {total_duration:.1f}s")
        
        # Бэкап камеры игрока
        backup_pos = np.copy(self.camera.pos)
        backup_yaw = self.camera.yaw
        backup_pitch = self.camera.pitch
        
        try:
            writer = imageio.get_writer(filename, fps=fps, macro_block_size=None)
            fixed_dt = 1.0 / 60.0
            self.is_rendering_video = True 
            
            for frame_num in range(total_frames):
                t = frame_num * fixed_dt
                
                # 1. Обновляем камеру по сплайну
                pos, yaw, pitch = path.get_interpolated_state(t)
                self.camera.pos = pos
                self.camera.yaw = yaw
                self.camera.pitch = pitch
                self.camera.update_vectors()
                
                # 2. Обновляем мир
                self.texture_manager.update(fixed_dt)
                # Передаем текущую скорость солнца для облаков
                self.cloud_renderer.update(fixed_dt, self.sun_speed)
                
                # 3. Рисуем кадр
                self._render_frame(fixed_dt)
                
                # 4. Читаем пиксели
                width, height = self.draw_w, self.draw_h
                buffer = glReadPixels(0, 0, width, height, GL_RGB, GL_UNSIGNED_BYTE)
                image = np.frombuffer(buffer, dtype=np.uint8).reshape((height, width, 3))
                image = np.flipud(image)
                
                writer.append_data(image)
                
                # 5. Рисуем прогресс
                ui_proj = MatrixUtils.ortho_2d(0, self.win_w, self.win_h, 0)
                glDisable(GL_DEPTH_TEST)
                self.solid_renderer.add_quad_2d(0, self.win_h - 20, self.win_w * (frame_num / total_frames), 20, (1, 0, 0, 1))
                self.solid_renderer.flush(MatrixUtils.identity(), ui_proj)
                
                sdl2.SDL_GL_SwapWindow(self.window)
                sdl2.SDL_PumpEvents()
                
                # Выход по Escape
                keys = sdl2.SDL_GetKeyboardState(None)
                if keys[sdl2.SDL_SCANCODE_ESCAPE]:
                    break

            writer.close()
        except Exception as e:
            print(f"Render Error: {e}")
            traceback.print_exc() # Выведет полную информацию в консоль
            self.show_notification(self.tr('NOTIF_RENDER_ERR'))
        finally:
            self.is_rendering_video = False
            
            # Восстанавливаем камеру
            self.camera.pos = backup_pos
            self.camera.yaw = backup_yaw
            self.camera.pitch = backup_pitch
            self.camera.update_vectors()
            
            # --- УСИЛЕННЫЙ ВОЗВРАТ МЫШИ ---
            # 1. Сначала явно разблокируем, чтобы сбросить внутреннее состояние SDL
            self.set_mouse_lock(False)
            
            # 2. Центрируем мышь физически (чтобы не было резкого рывка)
            sdl2.SDL_WarpMouseInWindow(self.window, self.win_w // 2, self.win_h // 2)
            
            # 3. Сбрасываем накопленное смещение ввода
            self.input.reset_per_frame()
            
            # 4. Блокируем заново. ТЕПЕРЬ ЭТО СРАБОТАЕТ, т.к. self.file_dialog.active = False
            self.set_mouse_lock(True)
            # ------------------------------
            
            self.show_notification(self.tr('NOTIF_RENDER_DONE'))

    def update_chunks(self, force_radius=None, render_radius=None):
        if render_radius is None:
            render_radius = int(self.fog_distance / self.CHUNK_SIZE) + 2
        render_radius = max(2, render_radius)
        if not hasattr(self, 'last_used_render_radius'):
            self.last_used_render_radius = render_radius
        if render_radius != self.last_used_render_radius:
            self.force_chunk_update = True
            self.last_used_render_radius = render_radius
        px, py, pz = self.camera.pos
        cx, cy, cz = self.get_chunk_coords(px, pz, py)
        current_coord = (cx, cy, cz)
        self.floor_renderer.update(cx, cz, render_radius)
        if current_coord == self.last_chunk_coord and not self.force_chunk_update and not force_radius:
            return
        existing_chunks = list(self.chunk_meshes.keys())
        unload_dist_sq = (render_radius + 2) ** 2
        for coord in existing_chunks:
            tx, ty, tz = coord
            dist_sq = (tx - cx)**2 + (ty - cy)**2 + (tz - cz)**2
            if dist_sq > unload_dist_sq:
                mesh_dict = self.chunk_meshes[coord]
                for mesh in mesh_dict.values():
                    mesh.delete()
                # -------------------------------------------------------
                
                del self.chunk_meshes[coord]
                if coord in self.compiled_chunks:
                    self.compiled_chunks.remove(coord)
        self.chunk_load_queue = []
        self.last_chunk_coord = current_coord
        self.force_chunk_update = False
        candidates = []
        radius_y = 6 
        for dx in range(-render_radius, render_radius + 1):
            for dz in range(-render_radius, render_radius + 1):
                if dx*dx + dz*dz > render_radius*render_radius: continue
                target_cx = cx + dx
                target_cz = cz + dz
                for dy in range(-radius_y, radius_y + 1):
                    target_cy = cy + dy
                    coord = (target_cx, target_cy, target_cz)
                    if coord in self.compiled_chunks: continue
                    has_entities = coord in self.spatial_grid
                    if not has_entities:
                        self.compiled_chunks.add(coord)
                        continue
                    candidates.append(coord)
        candidates.sort(key=lambda c: (c[0]-cx)**2 + (c[1]-cy)**2 + (c[2]-cz)**2)
        self.chunk_load_queue = candidates
        if self.chunk_load_queue:
            start_time = pygame.time.get_ticks()
            time_budget = 20 if force_radius else 4 
            processed_count = 0
            while self.chunk_load_queue:
                if processed_count > 0 and (pygame.time.get_ticks() - start_time >= time_budget):
                    break
                chunk_coord = self.chunk_load_queue.pop(0)
                if chunk_coord not in self.compiled_chunks:
                    self.compile_single_chunk(*chunk_coord)
                    processed_count += 1
    def invalidate_chunk(self, cx, cy, cz):
        coord = (cx, cy, cz)
        if coord in self.chunk_meshes:
            mesh_dict = self.chunk_meshes[coord]
            for mesh in mesh_dict.values():
                mesh.delete()
            del self.chunk_meshes[coord]
        if coord in self.compiled_chunks:
            self.compiled_chunks.remove(coord)
    def invalidate_entity_chunks(self, ent):
        if ent.uid in self.large_objects_gl_cache:
            mesh_dict = self.large_objects_gl_cache[ent.uid]
            for mesh in mesh_dict.values():
                mesh.delete()
            del self.large_objects_gl_cache[ent.uid]
        
        half = ent.scale / 2.0
        
        # ДОБАВЛЕН MARGIN (Отступ)
        # Это гарантирует, что если объект стоит на границе чанка,
        # мы обновим и текущий, и соседний чанк.
        margin = 0.05 
        
        mn = ent.pos - half - margin
        mx = ent.pos + half + margin
        
        scx, scy, scz = self.get_chunk_coords(mn[0], mn[2], mn[1])
        ecx, ecy, ecz = self.get_chunk_coords(mx[0], mx[2], mx[1])
        
        for cx in range(scx, ecx + 1):
            for cy in range(scy, ecy + 1):
                for cz in range(scz, ecz + 1):
                    self.invalidate_chunk(cx, cy, cz)
    def close_color_picker(self, apply=True):
        if self.tex_session_active and self.selected_entities:
            if apply:
                full_data = self.color_picker.get_full_data()
                color_data = full_data[:6]
                tex_path = full_data[6]
                is_tiling = full_data[7]
                density_val = full_data[8]
                refl_val = full_data[9]
                self.last_paint_settings = {
                    'color': list(color_data), 
                    'all': self.color_picker.paint_all,
                    'is_tiling': is_tiling,
                    'density': density_val,
                    'reflectivity': refl_val, 
                    'texture_path': tex_path
                }
                self.apply_paint(color_data, self.color_picker.paint_all, is_tiling, density_val, tex_path, refl_val)
                self.color_picker.add_to_history()
                states_now = {e.uid: e.to_dict() for e in self.selected_entities}
                self.scene.push_modification(self.tex_session_start_states, states_now)
                self.mark_scene_changed(changed_entities=self.selected_entities)
            else:
                for uid, state_data in self.tex_session_start_states.items():
                    ent = self.scene.get_entity_by_uid(uid)
                    if ent:
                        ent.update_from_dict(state_data)
                        self.invalidate_entity_chunks(ent)
                self.force_chunk_update = True
        self.tex_session_active = False
        self.tex_session_start_states = {}
        self.local_tex_history = []
        self.local_tex_history_idx = -1
        self.color_picker.active = False
        if self.temp_selection:
            self.selected_entities = []
            self.selected_faces = {}
            self.temp_selection = False
        self.mouse_locked = True
        self.set_mouse_lock(True)
        self.input.mouse_rel = (0, 0)
        pygame.mouse.set_visible(False)
        pygame.mouse.get_rel()
    def get_face_index_from_norm(self, norm):
        if norm is None: return None
        if norm[0] > 0.5: return 0
        elif norm[0] < -0.5: return 1
        elif norm[1] > 0.5: return 2
        elif norm[1] < -0.5: return 3
        elif norm[2] > 0.5: return 4
        elif norm[2] < -0.5: return 5
        return None
    def auto_select_hovered(self):
        ray_o, ray_d = self.get_world_ray()
        cands = self.get_candidates_for_ray(ray_o, ray_d)
        ent, _, norm = self.scene.raycast(ray_o, ray_d, ignore_holes=True, candidates=cands)
        if ent and norm is not None:
            self.selected_entities = [ent]
            face_idx = self.get_face_index_from_norm(norm)
            if face_idx is not None:
                self.selected_faces = {ent: {face_idx}}
            return True
        return False
    def apply_paint(self, color, paint_all, is_tiling=False, density=1.0, texture_path=None, reflectivity=0.0):
        if not self.selected_entities: return
        states_before = {e.uid: e.to_dict() for e in self.selected_entities}
        changes_made = False
        if texture_path:
            self.texture_manager.load_from_file(texture_path)
        for ent in self.selected_entities:
            if ent.is_hole:
                continue
            new_colors = copy.deepcopy(ent.faces_colors)
            new_textures = list(ent.faces_textures)
            new_tiling = list(ent.faces_tiling)
            new_reflectivity = list(ent.faces_reflectivity) 
            modified = False
            if abs(ent.density - density) > 0.001:
                ent.density = density
                modified = True
            faces_to_process = range(6)
            if not paint_all:
                if ent in self.selected_faces and self.selected_faces[ent]:
                    faces_to_process = self.selected_faces[ent]
            for f_idx in faces_to_process:
                if new_colors[f_idx] != list(color):
                    new_colors[f_idx] = list(color)
                    modified = True
                if texture_path is not None:
                    if new_textures[f_idx] != texture_path:
                        new_textures[f_idx] = texture_path
                        modified = True
                if new_tiling[f_idx] != is_tiling:
                    new_tiling[f_idx] = is_tiling
                    modified = True
                if abs(new_reflectivity[f_idx] - reflectivity) > 0.001:
                    new_reflectivity[f_idx] = reflectivity
                    modified = True
            if modified:
                ent.faces_colors = new_colors
                ent.faces_textures = new_textures
                ent.faces_tiling = new_tiling
                ent.faces_reflectivity = new_reflectivity 
                changes_made = True
                self.invalidate_entity_chunks(ent)
        if changes_made:
            states_after = {e.uid: e.to_dict() for e in self.selected_entities}
            self.scene.push_modification(states_before, states_after)
            self.mark_scene_changed(changed_entities=self.selected_entities)
    def _render_reflection_pass(self, mirror_ent, target_fbo, axis, sign, override_plane_point=None, override_plane_normal=None):
        # 1. Определяем плоскость отражения (статическая или динамическая)
        if override_plane_point is not None and override_plane_normal is not None:
            plane_point = override_plane_point
            normal = override_plane_normal
        else:
            # Старая логика для статики
            min_p, max_p = mirror_ent.get_aabb()
            center = (min_p + max_p) / 2.0
            normal = np.zeros(3)
            normal[axis] = sign
            plane_point = center.copy()
            plane_point[axis] += (mirror_ent.scale[axis] / 2.0) * sign

        # 2. Плоскость отсечения (Clip Plane)
        dist_plane = -np.dot(normal, plane_point)
        # Немного сдвигаем, чтобы не артефачило саму поверхность зеркала
        clip_plane_val = dist_plane - 0.05 
        clip_plane = np.array([normal[0], normal[1], normal[2], clip_plane_val], dtype=np.float32)

        # 3. Расчет матрицы отражения камеры
        cam_dist = np.dot(self.camera.pos, normal) + dist_plane # Используем чистое расстояние
        mirrored_pos = self.camera.pos - 2.0 * (np.dot(self.camera.pos, normal) + dist_plane) * normal
        
        # Отражаем векторы ориентации
        mirrored_front = self.camera.front - 2.0 * np.dot(self.camera.front, normal) * normal
        mirrored_up = self.camera.up - 2.0 * np.dot(self.camera.up, normal) * normal
        
        aspect = self.draw_w / self.draw_h if self.draw_h > 0 else 1.0
        reflection_dist = 200.0 
        proj_mat = MatrixUtils.perspective(FOV, aspect, NEAR_CLIP, reflection_dist)
        # Инвертируем X в проекции, чтобы отразить картинку (стандартный трюк OpenGL зеркал)
        proj_mat[0, 0] *= -1.0
        
        target = mirrored_pos + mirrored_front
        view_mat = MatrixUtils.look_at(mirrored_pos, target, mirrored_up)

        # 4. Рендер в FBO
        target_fbo.bind()
        glClearColor(*self.current_sky_color, 1.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        glCullFace(GL_FRONT) # Инвертируем отсечение граней, так как мир вывернут
        
        # Фон (Звезды и Светила)
        self.star_renderer.draw(view_mat, proj_mat, mirrored_pos, self.sun_angle_time, self.sun_angle_tilt, self.sun_rotation_y, self.light_intensity)
        self.draw_celestial_bodies(view_mat, proj_mat)
        
        # Шейдер и Чанки
        self.shader.use()
        self.shader.set_mat4("projection", proj_mat)
        self.shader.set_mat4("view", view_mat)
        glUniform3f(glGetUniformLocation(self.shader.program, "viewPos"), *mirrored_pos)
        
        glEnable(GL_CLIP_PLANE0) 
        glUniform4f(glGetUniformLocation(self.shader.program, "uClipPlane"), *clip_plane)
        
        self._render_chunks_modern(
            cull_pos=mirrored_pos, 
            override_view=view_mat, 
            override_proj=proj_mat, 
            skip_ent=mirror_ent # Не рисуем само зеркало в отражении
        )
        self.shader.use()

        # --- НОВОЕ: Рисуем анимированные двери ВНУТРИ зеркала ---
        if self.door_animations:
             # Мы используем ту же геометрию, что и в основном кадре
             # Важно: шейдер уже активен, clip plane активен
             door_batches = self._generate_lit_door_geometry()
             glEnable(GL_BLEND); glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
             for (tex_id, mode), data_array in door_batches.items():
                if len(data_array) == 0: continue
                glActiveTexture(GL_TEXTURE0); glBindTexture(GL_TEXTURE_2D, tex_id)
                glUniform1i(glGetUniformLocation(self.shader.program, "uTexType"), mode)
                mesh = MeshBuffer(data_array)
                mesh.draw()
                mesh.delete()
             glDisable(GL_BLEND)
        # --------------------------------------------------------

        self.shader.use() 
        glDisable(GL_CLIP_PLANE0)
        glUniform4f(glGetUniformLocation(self.shader.program, "uClipPlane"), 0, 0, 0, 0)
        
        # Облака
        fog_val = self.fog_distance if hasattr(self, 'fog_distance') else 100.0
        dt_val = self.clock.get_time() / 1000.0 
        self.cloud_renderer.draw(view_mat, proj_mat, mirrored_pos, self.light_color, self.light_intensity, dt_val, fog_val)
        
        glCullFace(GL_BACK) # Возвращаем отсечение
        target_fbo.unbind(self.draw_w, self.draw_h)
    def update_window_mode(self, w, h):
        dw, dh = ctypes.c_int(), ctypes.c_int()
        sdl2.SDL_GL_GetDrawableSize(self.window, dw, dh)
        self.draw_w, self.draw_h = dw.value, dh.value
        self.win_w, self.win_h = w, h
        glViewport(0, 0, self.draw_w, self.draw_h)
        if hasattr(self, 'reflection_fbos'):
            for fbo in self.reflection_fbos:
                fbo.resize(self.draw_w, self.draw_h)
        self.create_ui()
        if hasattr(self, 'color_picker'):
            self.color_picker.rect.x = self.win_w - 320
        if hasattr(self, 'file_dialog'):
            self.file_dialog.update_layout(self.win_w, self.win_h, self.font)
    def set_mouse_lock(self, locked):
        if hasattr(self, 'file_dialog') and self.file_dialog.active:
            locked = False
        self.mouse_locked = locked
        if locked:
            sdl2.SDL_ShowCursor(sdl2.SDL_DISABLE)
            sdl2.SDL_SetRelativeMouseMode(sdl2.SDL_TRUE)
        else:
            sdl2.SDL_ShowCursor(sdl2.SDL_ENABLE)
            sdl2.SDL_SetRelativeMouseMode(sdl2.SDL_FALSE)
    def get_world_ray(self):
        mx, my = self.input.mouse_pos
        if self.mouse_locked:
            mx, my = self.win_w / 2, self.win_h / 2
        real_y = self.win_h - my 
        aspect = self.draw_w / self.draw_h if self.draw_h > 0 else 1.0
        proj = MatrixUtils.perspective(FOV, aspect, NEAR_CLIP, FAR_CLIP)
        
        # --- ИЗМЕНЕНИЕ: Используем visual_y для расчета луча ---
        # Создаем временную позицию для "глаз"
        visual_pos = np.copy(self.camera.pos)
        visual_pos[1] = self.camera.visual_y
        
        target = visual_pos + self.camera.front
        view = MatrixUtils.look_at(visual_pos, target, np.array([0,1,0], dtype=np.float32))
        # -------------------------------------------------------

        viewport = (0, 0, self.win_w, self.win_h)
        start = MatrixUtils.unproject(mx, real_y, 0.0, view, proj, viewport)
        end   = MatrixUtils.unproject(mx, real_y, 1.0, view, proj, viewport)
        if start is None or end is None:
            return np.array([0,0,0]), np.array([0,0,1])
        direction = normalize(end - start)
        return np.array(start), np.array(direction)
    def show_notification(self, text):
        self.notification_text = text
        self.notification_timer = pygame.time.get_ticks()
    def attempt_action(self, action_type):
        self.pending_exit_action = action_type
        if not self.unsaved_changes:
             self.finalize_action()
             return
        self.set_state("CONFIRM_SAVE")
    def finalize_action(self):
        act = self.pending_exit_action 
        if act == 'QUIT':
            self.running = False
        elif act == 'MENU':
            self.set_state("MENU")
        elif act == 'LOAD':
            self.io_load()
            if self.project_active:
                self.set_state("GAME")
        elif act == 'NEW':
            self._reset_project()
        self.pending_exit_action = None
    def perform_rect_selection(self, start_pos, end_pos, add_to_selection):
        x1, y1 = start_pos
        x2, y2 = end_pos
        is_crossing_selection = (x1 > x2)
        rect_min_x, rect_max_x = min(x1, x2), max(x1, x2)
        rect_min_y, rect_max_y = min(y1, y2), max(y1, y2)
        aspect = self.draw_w / self.draw_h if self.draw_h > 0 else 1.0
        proj = MatrixUtils.perspective(FOV, aspect, NEAR_CLIP, FAR_CLIP)
        target = self.camera.pos + self.camera.front
        view = MatrixUtils.look_at(self.camera.pos, target, np.array([0,1,0], dtype=np.float32))
        viewport = (0, 0, self.win_w, self.win_h)
        new_candidates = []
        for ent in self.scene.entities:
            if ent.is_animating: continue
            min_p, max_p = ent.get_aabb()
            corners_3d = [
                [min_p[0], min_p[1], min_p[2]], [max_p[0], min_p[1], min_p[2]],
                [min_p[0], max_p[1], min_p[2]], [max_p[0], max_p[1], min_p[2]],
                [min_p[0], min_p[1], max_p[2]], [max_p[0], min_p[1], max_p[2]],
                [min_p[0], max_p[1], max_p[2]], [max_p[0], max_p[1], max_p[2]]
            ]
            screen_xs = []
            screen_ys = []
            for p in corners_3d:
                res = MatrixUtils.project(p[0], p[1], p[2], view, proj, viewport)
                if res:
                    sx, sy, sz = res
                    if 0.0 <= sz <= 1.0:
                        real_sy = self.win_h - sy
                        screen_xs.append(sx)
                        screen_ys.append(real_sy)
            if not screen_xs:
                continue
            obj_min_x, obj_max_x = min(screen_xs), max(screen_xs)
            obj_min_y, obj_max_y = min(screen_ys), max(screen_ys)
            should_select = False
            if is_crossing_selection:
                overlap_x = (rect_min_x < obj_max_x) and (rect_max_x > obj_min_x)
                overlap_y = (rect_min_y < obj_max_y) and (rect_max_y > obj_min_y)
                if overlap_x and overlap_y:
                    should_select = True
            else:
                inside_x = (obj_min_x >= rect_min_x) and (obj_max_x <= rect_max_x)
                inside_y = (obj_min_y >= rect_min_y) and (obj_max_y <= rect_max_y)
                if inside_x and inside_y:
                    should_select = True
            if should_select:
                new_candidates.append(ent)
        if not add_to_selection:
             self.selected_entities = new_candidates
             self.selected_faces = {} 
        else:
             for ent in new_candidates:
                 if ent in self.selected_entities: 
                     self.selected_entities.remove(ent)
                     if ent in self.selected_faces: del self.selected_faces[ent]
                 else: 
                     self.selected_entities.append(ent)
    def rotate_selection(self):
        if not self.selected_entities: return
        axis = self.transform_axis 
        for ent in self.selected_entities:
            if ent.is_hole and axis != 1:
                return
        states_before = {e.uid: e.to_dict() for e in self.selected_entities}
        for ent in self.selected_entities:
            self.invalidate_entity_chunks(ent)
        corners_s = [[-1, 1, 1], [1, 1, 1], [1, -1, 1], [-1, -1, 1], [-1, 1, -1], [1, 1, -1], [1, -1, -1], [-1, -1, -1]]
        edges_idx = [(0, 1), (1, 2), (2, 3), (3, 0), (4, 5), (5, 6), (6, 7), (7, 4), (0, 4), (1, 5), (2, 6), (3, 7)]
        min_p = np.array([np.inf, np.inf, np.inf]); max_p = np.array([-np.inf, -np.inf, -np.inf])
        for ent in self.selected_entities:
            min_p = np.minimum(min_p, ent.pos); max_p = np.maximum(max_p, ent.pos)
        pivot = (min_p + max_p) / 2.0; pivot = snap_vector(pivot, 0.01)
        axis = self.transform_axis
        for ent in self.selected_entities:
            current_hinge_corners = None
            if ent.is_door and ent.hinge_edge != -1: current_hinge_corners = edges_idx[ent.hinge_edge]
            rel_pos = ent.pos - pivot; new_rel = np.copy(rel_pos); new_scale = np.copy(ent.scale)
            if axis == 1:
                new_rel[0] = rel_pos[2]; new_rel[2] = -rel_pos[0]; new_scale[0] = ent.scale[2]; new_scale[2] = ent.scale[0]
            elif axis == 0:
                new_rel[1] = -rel_pos[2]; new_rel[2] = rel_pos[1]; new_scale[1] = ent.scale[2]; new_scale[2] = ent.scale[1]
            elif axis == 2:
                new_rel[0] = -rel_pos[1]; new_rel[1] = rel_pos[0]; new_scale[0] = ent.scale[1]; new_scale[1] = ent.scale[0]
            ent.pos = pivot + new_rel; ent.scale = new_scale; ent.pos, ent.scale = snap_bounds_to_grid_3d(ent.pos, ent.scale, precision=0.01)
            TextureUtils.rotate_entity_data(ent, axis, direction=1)
            if current_hinge_corners is not None:
                v1 = list(corners_s[current_hinge_corners[0]]); v2 = list(corners_s[current_hinge_corners[1]])
                def transform_vec(v, ax):
                    nv = list(v)
                    if ax == 1: nv[0] = v[2]; nv[2] = -v[0]
                    elif ax == 0: nv[1] = -v[2]; nv[2] = v[1]
                    elif ax == 2: nv[0] = -v[1]; nv[1] = v[0]
                    return nv
                nv1 = transform_vec(v1, axis); nv2 = transform_vec(v2, axis)
                try:
                    new_idx1 = corners_s.index(nv1); new_idx2 = corners_s.index(nv2)
                    new_edge = -1
                    if (new_idx1, new_idx2) in edges_idx: new_edge = edges_idx.index((new_idx1, new_idx2))
                    elif (new_idx2, new_idx1) in edges_idx: new_edge = edges_idx.index((new_idx2, new_idx1))
                    ent.hinge_edge = new_edge
                except ValueError: pass
        states_after = {e.uid: e.to_dict() for e in self.selected_entities}
        current_time = pygame.time.get_ticks()
        merged = False
        if current_time - self.last_action_timestamp < 800:
            merged = self.scene.merge_last_modification(states_after)
        if not merged:
            self.scene.push_modification(states_before, states_after)
        self.last_action_timestamp = current_time
        self.mark_scene_changed(changed_entities=self.selected_entities)
    def mirror_selection(self):
        if not self.selected_entities: return
        for ent in self.selected_entities:
            if ent.is_hole:
                return
        states_before = {e.uid: e.to_dict() for e in self.selected_entities}
        for ent in self.selected_entities:
            self.invalidate_entity_chunks(ent)
        corners_s = [[-1, 1, 1], [1, 1, 1], [1, -1, 1], [-1, -1, 1],
                     [-1, 1, -1], [1, 1, -1], [1, -1, -1], [-1, -1, -1]]
        edges_idx = [(0, 1), (1, 2), (2, 3), (3, 0), 
                     (4, 5), (5, 6), (6, 7), (7, 4), 
                     (0, 4), (1, 5), (2, 6), (3, 7)]
        min_p = np.array([np.inf, np.inf, np.inf])
        max_p = np.array([-np.inf, -np.inf, -np.inf])
        for ent in self.selected_entities:
            min_p = np.minimum(min_p, ent.pos)
            max_p = np.maximum(max_p, ent.pos)
        pivot = (min_p + max_p) / 2.0
        pivot = snap_vector(pivot, 0.01)
        axis = self.transform_axis
        for ent in self.selected_entities:
            current_hinge_corners = None
            if ent.is_door and ent.hinge_edge != -1:
                current_hinge_corners = edges_idx[ent.hinge_edge]
            ent.pos[axis] = 2 * pivot[axis] - ent.pos[axis]
            ent.pos, ent.scale = snap_bounds_to_grid_3d(ent.pos, ent.scale, precision=0.01)
            TextureUtils.mirror_entity_data(ent, axis)
            if current_hinge_corners is not None:
                v1 = list(corners_s[current_hinge_corners[0]])
                v2 = list(corners_s[current_hinge_corners[1]])
                v1[axis] = -v1[axis]
                v2[axis] = -v2[axis]
                try:
                    new_idx1 = corners_s.index(v1)
                    new_idx2 = corners_s.index(v2)
                    new_edge = -1
                    if (new_idx1, new_idx2) in edges_idx: new_edge = edges_idx.index((new_idx1, new_idx2))
                    elif (new_idx2, new_idx1) in edges_idx: new_edge = edges_idx.index((new_idx2, new_idx1))
                    ent.hinge_edge = new_edge
                except ValueError: pass
        states_after = {e.uid: e.to_dict() for e in self.selected_entities}
        self.scene.push_modification(states_before, states_after)
        self.mark_scene_changed(changed_entities=self.selected_entities)
    def set_state(self, new_state):
        self.state = new_state
        # Добавляем CINECAM в список режимов с захватом мыши
        if new_state == "GAME" or new_state == "SUN_SETTINGS" or new_state == "CINECAM":
            self.set_mouse_lock(True)
        else:
            self.set_mouse_lock(False)
    def toggle_game_mode(self):
        # Если сейчас Творческий режим (переключаемся в Приключение)
        if self.creative_mode:
            # --- НОВОЕ: Запоминаем, были ли мы в режиме камеры ---
            if self.state == "CINECAM":
                self.was_in_cinecam = True
                self.set_state("GAME") # Принудительно выходим в обычный режим (убираем интерфейс камер)
            else:
                self.was_in_cinecam = False
            # -----------------------------------------------------

            self.creative_mode = False # Переключаем флаг

            # --- Старая логика настройки Приключения (ПОЛНОСТЬЮ СОХРАНЕНА) ---
            self.saved_creative_speed = self.camera.speed 
            self.camera.speed = self.fixed_adventure_speed
            self.vertical_velocity = 0 
            self.player_height = self.stand_height
            self.camera.visual_y = self.camera.pos[1]
            self.current_sky_color = COLOR_NIGHT
            self.saved_creative_tool = self.tool_mode
            self.tool_mode = 'SELECT'
            self.edit_mode = True 
            self.build_start = None
            self.cut_start_point = None
            self.room_extruding = False
            self.selected_entities = [] 
            self.build_spatial_grid()
            self.compile_large_entities() 
            self.update_chunks(force_radius=True, render_radius=12)

        # Если сейчас Приключение (переключаемся в Творческий)
        else:
            self.creative_mode = True # Переключаем флаг

            # --- Старая логика восстановления Творческого ---
            self.camera.speed = self.saved_creative_speed
            self.camera.visual_y = self.camera.pos[1]
            self.current_sky_color = COLOR_SKY
            self.tool_mode = self.saved_creative_tool if self.saved_creative_tool else 'SELECT'
            
            # --- НОВОЕ: Восстановление режима камеры ---
            if self.was_in_cinecam:
                self.set_state("CINECAM")
                self.tool_mode = 'SELECT' # Сбрасываем инструмент, чтобы не мешал
                self.show_notification("CINE CAMERA MODE: RESTORED")
            # -------------------------------------------

            # --- Окончание старой логики ---
            self.build_spatial_grid()
            self.update_chunks(force_radius=True, render_radius=24)
    def mark_scene_changed(self, changed_entities=None):
        self.unsaved_changes = True
        self.build_spatial_grid()
        self.cached_large_entities = []
        for ent in self.scene.entities:
            if max(ent.scale) > self.CHUNK_SIZE:
                self.cached_large_entities.append(ent)
        if changed_entities:
            for ent in changed_entities:
                self.invalidate_entity_chunks(ent)
            self.force_chunk_update = True
        else:
            self.compiled_chunks.clear()
            self.compile_large_entities() 
            self.force_chunk_update = True
    def create_ui(self):
        for attr_name in dir(self):
            attr = getattr(self, attr_name)
            if isinstance(attr, Widget) or isinstance(attr, TextLabel):
                attr.delete()
        if hasattr(self, 'tex_title_menu') and self.tex_title_menu: glDeleteTextures([self.tex_title_menu])
        if hasattr(self, 'tex_title_pause') and self.tex_title_pause: glDeleteTextures([self.tex_title_pause])
        
        win_w, win_h = self.win_w, self.win_h
        cx, cy = win_w // 2, win_h // 2
        scale_factor = win_h / 900.0
        
        # Шрифты пересоздаем, чтобы убедиться в поддержке символов (хотя Arial обычно ок)
        font_size = int(22 * scale_factor)
        self.font = pygame.font.SysFont('Arial', max(12, font_size))
        target_title_size = int(120 * scale_factor)
        self.title_font = pygame.font.SysFont('Arial', max(60, target_title_size))
        
        self.tex_title_menu, self.tw_menu, self.th_menu = safe_text_to_texture(self.tr('GAMENAME'), self.title_font)
        self.tex_title_pause, self.tw_pause, self.th_pause = safe_text_to_texture(self.tr('PAUSED'), self.title_font)
        
        self.lbl_confirm_question = TextLabel(self.title_font, (255, 255, 255))
        self.lbl_confirm_question.set_text(self.tr('SAVE_QUESTION'))
        
        self.lbl_mode = TextLabel(self.font)
        self.lbl_tool = TextLabel(self.font)
        self.lbl_snap = TextLabel(self.font)
        self.lbl_hint = TextLabel(self.font)
        self.lbl_fps = TextLabel(self.font, (255, 255, 0))
        self.lbl_fps.set_text("FPS: 0")
        
        cur_fog = self.fog_distance if hasattr(self, 'fog_distance') else 100
        cur_thick = self.default_thickness if hasattr(self, 'default_thickness') else 0.1
        
        # Callbacks (оставляем как есть)
        def action_toggle_fps():
            self.limit_fps = not self.limit_fps
            sdl2.SDL_GL_SetSwapInterval(1 if self.limit_fps else 0)
            self.create_ui()
        def action_resume_game(): self.set_state("GAME")
        def request_new(): self.attempt_action('NEW')
        def request_load(): self.attempt_action('LOAD')
        def request_quit(): self.attempt_action('QUIT')
        def request_menu(): self.attempt_action('MENU')
        def action_save(): 
            if self.current_filename: self._perform_save(self.current_filename)
            else: self.io_save()
        def action_export_menu():
            self.file_dialog.open('save', self.on_file_dialog_result, is_export=True)
        def action_clear_scene():
            self.scene.clear()
            
            # СБРОС ВСЕХ ПАРАМЕТРОВ (Солнце, Скорость, Инструменты)
            self._reset_simulation_state()
            
            # Очистка кешей
            for mesh_dict in self.chunk_meshes.values():
                for mesh in mesh_dict.values(): mesh.delete()
            self.chunk_meshes.clear()
            self.compiled_chunks.clear()
            
            for mesh_dict in self.large_objects_gl_cache.values():
                for mesh in mesh_dict.values(): mesh.delete()
            self.large_objects_gl_cache.clear()
            self.cached_large_entities = []
            
            self.mark_scene_changed()
            self.set_state("GAME")
        def confirm_save_yes():
            if self.current_filename: self._perform_save(self.current_filename)
            else: self.io_save()
        def confirm_save_no(): self.unsaved_changes = False; self.finalize_action()
        def confirm_save_cancel(): self.pending_exit_action = None; self.set_state("GAME")
        
        # --- Language Action ---
        def action_switch_lang():
            self.toggle_language()

        # UI Layout
        bw, bh = int(200 * scale_factor), int(50 * scale_factor)
        margin = int(20 * scale_factor)
        
        # Main Menu
        self.btn_main_resume = Button(cx - bw//2, cy - bh*2 - margin, bw, bh, self.tr('RESUME_PROJECT'), self.font, action_resume_game)
        self.btn_main_new = Button(cx - bw//2, cy - bh, bw, bh, self.tr('NEW_PROJECT'), self.font, request_new)
        self.btn_load_menu = Button(cx - bw//2, cy + margin, bw, bh, self.tr('LOAD_PROJECT'), self.font, request_load)
        # Кнопка языка в главном меню
        self.btn_lang_menu = Button(cx - bw//2, cy + margin*4.5, bw, bh, self.tr('LANGUAGE'), self.font, action_switch_lang)
        
        self.btn_quit_menu = Button(cx - bw//2, cy + margin*8.0, bw, bh, self.tr('QUIT'), self.font, request_quit)
        
        # Pause Menu
        py = int(160 * scale_factor)
        bh_s = int(40 * scale_factor)
        step = int(60 * scale_factor)
        
        self.btn_resume = Button(cx - bw//2, py, bw, bh_s, self.tr('RESUME'), self.font, action_resume_game)
        self.slider_fog = Slider(cx - int(150*scale_factor), py + step*1.1, int(300*scale_factor), int(20*scale_factor), 20, 500, cur_fog, self.tr('FOG_DIST'), self.font)
        self.slider_thick = Slider(cx - int(150*scale_factor), py + step*2.0, int(300*scale_factor), int(20*scale_factor), 0.01, 1.0, cur_thick, self.tr('WALL_THICK'), self.font)
        
        fps_text = self.tr('FPS_LIMIT_ON') if self.limit_fps else self.tr('FPS_LIMIT_OFF')
        self.btn_fps = Button(cx - bw//2, py + step*3.0, bw, bh_s, fps_text, self.font, action_toggle_fps)
        self.btn_save = Button(cx - bw//2, py + step*4.0, bw, bh_s, self.tr('SAVE_PROJECT'), self.font, action_save)
        self.btn_export = Button(cx - bw//2, py + step*5.0, bw, bh_s, self.tr('EXPORT_3D'), self.font, action_export_menu)
        self.btn_load = Button(cx - bw//2, py + step*6.0, bw, bh_s, self.tr('LOAD_PROJECT'), self.font, request_load)
        self.btn_clear = Button(cx - bw//2, py + step*7.0, bw, bh_s, self.tr('CLEAR_SCENE'), self.font, action_clear_scene)
        self.btn_menu = Button(cx - bw//2, py + step*8.0, bw, bh_s, self.tr('MAIN_MENU'), self.font, request_menu)
        self.btn_quit = Button(cx - bw//2, py + step*9.0, bw, bh_s, self.tr('QUIT'), self.font, request_quit)
        
        # Confirm Dialog
        dialog_shift = int(150 * scale_factor)
        dialog_cy = cy - dialog_shift
        yes_no_y_offset = int(180 * scale_factor)
        self.btn_confirm_yes = Button(cx - bw - 10, dialog_cy + yes_no_y_offset, bw, bh, self.tr('SAVE_EXIT'), self.font, confirm_save_yes)
        self.btn_confirm_no = Button(cx + 10, dialog_cy + yes_no_y_offset, bw, bh, self.tr('DONT_SAVE'), self.font, confirm_save_no)
        cancel_y_offset = int(260 * scale_factor)
        cancel_width = bw * 2 + 20 
        self.btn_confirm_cancel = Button(cx - cancel_width//2, dialog_cy + cancel_y_offset, cancel_width, bh, self.tr('CANCEL'), self.font, confirm_save_cancel)
    def apply_keyboard_manipulation(self, key, pressed_keys):
        step = 0.1
        if pressed_keys.get(sdl2.SDLK_LCTRL) or pressed_keys.get(sdl2.SDLK_RCTRL):
            step = 0.01
        elif pressed_keys.get(sdl2.SDLK_LSHIFT) or pressed_keys.get(sdl2.SDLK_RSHIFT):
            step = 1.0
        if not self.selected_entities: return
        states_before = {e.uid: e.to_dict() for e in self.selected_entities}
        for ent in self.selected_entities:
            self.invalidate_entity_chunks(ent)
        if self.manipulation_mode == 'MOVE':
            move_vec = np.zeros(3)
            if self.vertical_mode:
                if key == sdl2.SDLK_UP:    move_vec[1] = step
                if key == sdl2.SDLK_DOWN:  move_vec[1] = -step
            else:
                cam_front = self.camera.front
                if abs(cam_front[0]) > abs(cam_front[2]):
                    primary_axis = np.array([1, 0, 0]) if cam_front[0] > 0 else np.array([-1, 0, 0])
                    secondary_axis = np.array([0, 0, 1]) if cam_front[0] > 0 else np.array([0, 0, -1])
                else:
                    primary_axis = np.array([0, 0, 1]) if cam_front[2] > 0 else np.array([0, 0, -1])
                    secondary_axis = np.array([1, 0, 0])
                cam_right = self.camera.right
                if np.dot(cam_right, secondary_axis) < 0: secondary_axis = -secondary_axis
                if key == sdl2.SDLK_UP:    move_vec = primary_axis * step
                if key == sdl2.SDLK_DOWN:  move_vec = -primary_axis * step
                if key == sdl2.SDLK_RIGHT: move_vec = secondary_axis * step
                if key == sdl2.SDLK_LEFT:  move_vec = -secondary_axis * step
            for ent in self.selected_entities:
                if ent.is_hole:
                    final_move = move_vec.copy(); final_move[1] = 0.0
                    ent.pos += final_move; ent.pos[1] = 0.0
                else:
                    ent.pos += move_vec
                ent.pos, ent.scale = snap_bounds_to_grid_3d(ent.pos, ent.scale, precision=0.01)
        elif self.manipulation_mode == 'RESIZE':
            delta = 0
            if key in [sdl2.SDLK_UP, sdl2.SDLK_RIGHT]: delta = step
            if key in [sdl2.SDLK_DOWN, sdl2.SDLK_LEFT]: delta = -step
            if delta != 0:
                is_alt = pressed_keys.get(sdl2.SDLK_LALT) or pressed_keys.get(sdl2.SDLK_RALT)
                norm = self.push_pull_normal if self.push_pull_normal is not None else np.array([0, 1, 0])
                axis = np.argmax(np.abs(norm))
                sign = np.sign(norm[axis]); sign = 1 if sign == 0 else sign
                for ent in self.selected_entities:
                    if ent.is_hole and axis == 1: continue 
                    old_ent_sim = Entity(ent.pos.copy(), ent.scale.copy())
                    old_ent_sim.faces_uv_data = copy.deepcopy(ent.faces_uv_data)
                    old_ent_sim.faces_reflectivity = list(ent.faces_reflectivity) 
                    if is_alt:
                        uniform_delta = delta * 2.0
                        new_scale = ent.scale + uniform_delta
                        if ent.is_hole: new_scale[1] = 0.05
                        for i in range(3):
                            if new_scale[i] < 0.01: new_scale[i] = 0.01
                        ent.scale = new_scale
                        ent.pos, ent.scale = snap_bounds_to_grid_3d(ent.pos, ent.scale, precision=0.01)
                    else:
                        old_scale_val = ent.scale[axis]
                        target_scale = old_scale_val + delta
                        if target_scale < 0.01: target_scale = 0.01
                        diff = target_scale - old_scale_val
                        if abs(diff) < 0.0001: continue
                        ent.scale[axis] = target_scale
                        ent.pos[axis] += (diff / 2.0) * sign
                        ent.pos, ent.scale = snap_bounds_to_grid_3d(ent.pos, ent.scale, precision=0.01)
                    TextureUtils.preserve_texture_pos(old_ent_sim, ent)
        states_after = {e.uid: e.to_dict() for e in self.selected_entities}
        current_time = pygame.time.get_ticks()
        merged = False
        if current_time - self.last_action_timestamp < 600:
            merged = self.scene.merge_last_modification(states_after)
        if not merged:
            self.scene.push_modification(states_before, states_after)
        self.last_action_timestamp = current_time
        self.mark_scene_changed(changed_entities=self.selected_entities)
    def get_point_on_plane(self, ray_o, ray_d, plane_point, plane_normal):
        denom = np.dot(plane_normal, ray_d)
        if abs(denom) > 1e-6:
            t = np.dot(plane_normal, (plane_point - ray_o)) / denom
            return ray_o + ray_d * t
        return None
    def calculate_extrusion_height_generic(self, ray_o, ray_d, base_rect_or_p):
        norm = None
        if self.tool_mode == 'STRIP': norm = self.strip_normal
        current_raw = self.calculate_extrusion_raw(ray_o, ray_d, base_rect_or_p, norm)
        val = current_raw
        keys = self.input.get_keys()
        snap = 0.01 if (keys.get(sdl2.SDLK_LCTRL) or keys.get(sdl2.SDLK_RCTRL)) else self.snap_unit
        return snap_value(val, snap)
    def finalize_box(self, extrusion_val):
        p1 = self.box_base_rect['p1']
        p2 = self.box_base_rect['p2']
        p_min = np.minimum(p1, p2)
        p_max = np.maximum(p1, p2)
        size = p_max - p_min
        axis = self.constraint_axis
        base_center = (p_min + p_max) / 2.0
        final_center = base_center.copy()
        final_center[axis] += extrusion_val / 2.0
        final_size = size.copy()
        final_size[axis] = abs(extrusion_val)
        for i in range(3):
            if final_size[i] < 0.001: final_size[i] = 0.01
        new_ent = Entity(final_center, final_size)
        c = self.last_paint_settings['color']
        new_ent.faces_colors = [list(c)] * 6
        is_tiling_val = self.last_paint_settings.get('is_tiling', False)
        new_ent.faces_tiling = [is_tiling_val] * 6
        new_ent.density = self.last_paint_settings.get('density', 1.0)
        refl_val = self.last_paint_settings.get('reflectivity', 0.0)
        new_ent.faces_reflectivity = [refl_val] * 6 
        tex = self.last_paint_settings.get('texture_path', None)
        if tex:
            self.texture_manager.load_from_file(tex)
            new_ent.faces_textures = [tex] * 6
        self.scene.add_entity(new_ent)
        self.mark_scene_changed(changed_entities=[new_ent])
    def finalize_strip(self, height):
        if len(self.strip_points) < 2: return
        axis = np.argmax(np.abs(self.strip_normal))
        thickness = self.default_thickness
        c = self.last_paint_settings['color']
        is_tiling_setting = self.last_paint_settings.get('is_tiling', False)
        density_val = self.last_paint_settings.get('density', 1.0)
        refl_val = self.last_paint_settings.get('reflectivity', 0.0) 
        tex_path = self.last_paint_settings.get('texture_path', None)
        if tex_path:
            self.texture_manager.load_from_file(tex_path)
        created_entities = []
        is_closed = (np.linalg.norm(self.strip_points[-1] - self.strip_points[0]) < 0.001)
        num_segments = len(self.strip_points) - 1
        for i in range(num_segments):
            p_start = self.strip_points[i]
            p_end = self.strip_points[i+1]
            vec = p_end - p_start
            length = np.linalg.norm(vec)
            if length < 0.001: continue
            seg_axis = np.argmax(np.abs(vec)) 
            direction = vec / length
            extend_start = True
            extend_end = True
            if i == 0 and not is_closed:
                extend_start = False
            if i == num_segments - 1 and not is_closed:
                extend_end = False
            p_start_ext = p_start.copy()
            p_end_ext = p_end.copy()
            if extend_start:
                p_start_ext -= direction * (thickness / 2.0)
            if extend_end:
                p_end_ext += direction * (thickness / 2.0)
            new_vec = p_end_ext - p_start_ext
            new_length = np.linalg.norm(new_vec)
            center = (p_start_ext + p_end_ext) / 2.0
            center[axis] += height / 2.0
            size = np.array([thickness, thickness, thickness])
            size[axis] = abs(height)
            size[seg_axis] = new_length
            ent = Entity(center, size, group_id=None)
            ent.faces_colors = [list(c)] * 6
            ent.faces_tiling = [is_tiling_setting] * 6
            ent.density = density_val
            ent.faces_reflectivity = [refl_val] * 6
            if tex_path:
                ent.faces_textures = [tex_path] * 6
            self.scene.entities.append(ent)
            created_entities.append(ent)
        if len(created_entities) >= 2 and is_closed:
            first_ent = created_entities[0]
            last_ent = created_entities[-1]
            vec_centers = last_ent.pos - first_ent.pos
            dist_centers = np.linalg.norm(vec_centers)
            if dist_centers > 0.001:
                dir_centers = vec_centers / dist_centers
                is_axis_aligned = False
                aligned_axis = -1
                for k in range(3):
                    if abs(abs(dir_centers[k]) - 1.0) < 0.001:
                        is_axis_aligned = True
                        aligned_axis = k
                        break
                if is_axis_aligned:
                    min_f, max_f = first_ent.get_aabb()
                    min_l, max_l = last_ent.get_aabb()
                    union_min = np.minimum(min_f, min_l)
                    union_max = np.maximum(max_f, max_l)
                    union_size = union_max - union_min
                    matches_other_axes = True
                    for k in range(3):
                        if k != aligned_axis:
                            if abs(union_size[k] - first_ent.scale[k]) > 0.001:
                                matches_other_axes = False
                                break
                    if matches_other_axes:
                        self.scene.entities.remove(first_ent)
                        self.scene.entities.remove(last_ent)
                        if first_ent in created_entities: created_entities.remove(first_ent)
                        if last_ent in created_entities: created_entities.remove(last_ent)
                        new_center = (union_min + union_max) / 2.0
                        new_size = union_max - union_min
                        new_ent = Entity(new_center, new_size, group_id=None)
                        new_ent.faces_colors = first_ent.faces_colors 
                        new_ent.faces_tiling = [is_tiling_setting] * 6
                        new_ent.density = density_val
                        new_ent.faces_reflectivity = [refl_val] * 6
                        if tex_path:
                            new_ent.faces_textures = [tex_path] * 6
                        self.scene.entities.append(new_ent)
                        created_entities.append(new_ent)
        if created_entities:
            self.scene.push_transaction(
                added_ents=created_entities, 
                removed_ents=[], 
                modified_triplets=[]
            )
            self.mark_scene_changed(changed_entities=created_entities)
    def get_ground_intersect(self, origin, direction):
        if direction[1] == 0: return None
        t = -origin[1] / direction[1]
        if t < 0: return None
        return origin + direction * t
    def exit_rect_selection(self):
        self.set_mouse_lock(True)
        self.input.mouse_rel = (0, 0)
        self.mouse_locked = True
        pygame.event.set_grab(True)
        pygame.mouse.set_visible(False)
        pygame.mouse.get_rel() 
    def update_adventure_physics(self, keys, dt):
        if dt > 0.1: dt = 0.1
        px, py, pz = self.camera.pos
        center_y = py - self.player_height * 0.5
        current_medium_density = 0.0
        in_hole = False
        lowest_entity_y = 0.0
        candidates = self.get_nearby_entities(px, pz, radius=1, py=center_y)
        for ent in candidates:
            if not ent.is_hole and not ent.is_animating:
                min_p, max_p = ent.get_aabb()
                eps = 0.05
                if (px > min_p[0] + eps and px < max_p[0] - eps and
                    center_y > min_p[1] + eps and center_y < max_p[1] - eps and
                    pz > min_p[2] + eps and pz < max_p[2] - eps):
                    if ent.density > current_medium_density:
                        current_medium_density = ent.density
            bottom_y = ent.pos[1] - ent.scale[1]/2.0
            if bottom_y < lowest_entity_y: lowest_entity_y = bottom_y
            if ent.is_hole:
                half = ent.scale / 2.0
                margin = 0.1 
                if (px > ent.pos[0] - half[0] + margin and px < ent.pos[0] + half[0] - margin and
                    pz > ent.pos[2] - half[2] + margin and pz < ent.pos[2] + half[2] - margin):
                    in_hole = True
        can_swim = (current_medium_density >= 0.25 and current_medium_density < 0.99)
        is_crouch = keys.get(sdl2.SDLK_LSHIFT) or keys.get(sdl2.SDLK_RSHIFT)
        is_sprint = keys.get(sdl2.SDLK_LCTRL) or keys.get(sdl2.SDLK_RCTRL)
        target_h = self.crouch_height if is_crouch else self.stand_height
        diff = target_h - self.player_height
        self.player_height += diff * 10.0 * dt
        if is_crouch: speed = self.crouch_speed
        elif is_sprint: speed = self.sprint_speed
        else: speed = self.fixed_adventure_speed
        movement_difficulty = max(0.05, 1.0 - current_medium_density)
        speed *= movement_difficulty
        if can_swim:
            drag_factor = 2.0 + (current_medium_density * 15.0) 
            self.vertical_velocity *= (1.0 - min(1.0, drag_factor * dt))
            buoyancy_factor = (1.0 - current_medium_density)
            effective_gravity = self.gravity * buoyancy_factor * movement_difficulty
            self.vertical_velocity -= effective_gravity * dt 
            base_swim_power = 30.0 
            final_swim_force = base_swim_power * movement_difficulty
            if keys.get(sdl2.SDLK_SPACE): 
                self.vertical_velocity += final_swim_force * dt
            if is_crouch: 
                self.vertical_velocity -= final_swim_force * dt
            self.camera.pos[1] += self.vertical_velocity * dt
            self.is_grounded = False 
            feet_y = self.camera.pos[1] - self.player_height
            if not in_hole and feet_y < 0:
                self.camera.pos[1] = self.player_height
                self.vertical_velocity = max(0, self.vertical_velocity)
            collision_candidates = self.get_nearby_entities(px, pz, radius=1, py=feet_y)
            for ent in collision_candidates:
                if ent.is_hole or ent.is_animating: continue
                if ent.density < 0.99: continue 
                min_p, max_p = ent.get_aabb()
                if (px > min_p[0] and px < max_p[0] and
                    pz > min_p[2] and pz < max_p[2]):
                    if feet_y < max_p[1] and feet_y > min_p[1] - 0.5:
                        self.camera.pos[1] = max_p[1] + self.player_height
                        self.vertical_velocity = max(0, self.vertical_velocity)
        else:
            self.vertical_velocity -= self.gravity * dt
            self.camera.pos[1] += self.vertical_velocity * dt
            self.is_grounded = False
            self.resolve_stuck()
            feet_y = self.camera.pos[1] - self.player_height
            should_collide_with_global_floor = (not in_hole) and (feet_y > -0.5)
            if should_collide_with_global_floor:
                if feet_y < 0:
                    self.camera.pos[1] = self.player_height
                    self.vertical_velocity = 0
                    self.is_grounded = True
            if self.is_grounded and self.vertical_velocity == 0:
                surface_h = self._get_surface_height(self.camera.pos[0], self.camera.pos[2])
                if abs(surface_h - (self.camera.pos[1] - self.player_height)) < 0.1:
                    self.last_stable_pos = np.copy(self.camera.pos)
            if keys.get(sdl2.SDLK_SPACE) and self.is_grounded:
                self.vertical_velocity = self.jump_force
                self.is_grounded = False
                self.camera.pos[1] += 0.01
        limit_y = min(-20.0, lowest_entity_y - 10.0)
        if self.camera.pos[1] < limit_y:
            self.vertical_velocity = 0
            target_x, target_y, target_z = 0, 0, 0
            found_safe_spot = False
            check_h = self._get_surface_height(self.last_stable_pos[0], self.last_stable_pos[2])
            if check_h > -float('inf'):
                target_x = self.last_stable_pos[0]; target_z = self.last_stable_pos[2]; target_y = check_h
                found_safe_spot = True
                self.show_notification(self.tr('NOTIF_SAFE_SPOT'))
            if not found_safe_spot:
                search_radius = 1
                start_x, start_z = px, pz 
                while not found_safe_spot and search_radius < 50:
                    for dx in range(-search_radius, search_radius + 1):
                        for dz in range(-search_radius, search_radius + 1):
                            if abs(dx) != search_radius and abs(dz) != search_radius: continue
                            check_x = start_x + dx; check_z = start_z + dz
                            h = self._get_surface_height(check_x, check_z)
                            if h > -float('inf'):
                                target_x = check_x; target_z = check_z; target_y = h
                                found_safe_spot = True
                                break
                        if found_safe_spot: break
                    search_radius += 1
                if found_safe_spot: self.show_notification(self.tr('NOTIF_RESPAWN'))
                else: self.show_notification(self.tr('NOTIF_EMERGENCY_RESPAWN'))
            self.camera.pos[0] = target_x
            self.camera.pos[2] = target_z
            self.camera.pos[1] = target_y + self.player_height + 0.2
            self.last_stable_pos = np.copy(self.camera.pos)
        self.resolve_stuck() 
        rad = math.radians(self.camera.yaw)
        c, s = math.cos(rad), math.sin(rad)
        fwd_x, fwd_z = c, s 
        rgt_x, rgt_z = -s, c
        move_x = 0; move_z = 0
        if keys.get(sdl2.SDLK_w): move_x += fwd_x; move_z += fwd_z
        if keys.get(sdl2.SDLK_s): move_x -= fwd_x; move_z -= fwd_z
        if keys.get(sdl2.SDLK_d): move_x += rgt_x; move_z += rgt_z
        if keys.get(sdl2.SDLK_a): move_x -= rgt_x; move_z -= rgt_z
        if move_x != 0 or move_z != 0:
            length = math.hypot(move_x, move_z)
            move_x /= length; move_z /= length
        self.camera.pos[0] += move_x * speed * dt
        self.camera.pos[2] += move_z * speed * dt
        self.resolve_stuck()
    def resolve_stuck(self):
        px, py, pz = self.camera.pos
        r = self.player_radius
        h = self.player_height
        pad = 0.002 
        min_px, max_px = px - r - pad, px + r + pad
        min_pz, max_pz = pz - r - pad, pz + r + pad
        min_py, max_py = py - h - pad, py + pad 
        step_height = 0.6 
        candidates = self.get_nearby_entities(px, pz, radius=1, py=py)
        for ent in candidates:
            if ent.is_hole: continue
            if ent.density < 0.99: continue
            half = ent.scale / 2.0
            min_ex, max_ex = ent.pos[0] - half[0], ent.pos[0] + half[0]
            min_ey, max_ey = ent.pos[1] - half[1], ent.pos[1] + half[1]
            min_ez, max_ez = ent.pos[2] - half[2], ent.pos[2] + half[2]
            if (max_px > min_ex and min_px < max_ex and
                max_py > min_ey and min_py < max_ey and
                max_pz > min_ez and min_pz < max_ez):
                d_left = max_px - min_ex
                d_right = max_ex - min_px
                d_down = max_py - min_ey 
                d_up = max_ey - min_py   
                d_back = max_pz - min_ez
                d_front = max_ez - min_pz
                min_horiz = min(d_left, d_right, d_back, d_front)
                feet_y = py - h
                rel_h = max_ey - feet_y
                if 0 < rel_h <= step_height and d_down > rel_h:
                    self.camera.pos[1] = max_ey + h + 0.001
                    if self.vertical_velocity < 0: self.vertical_velocity = 0
                    self.is_grounded = True
                    continue
                min_overlap = min(min_horiz, d_down, d_up)
                if min_overlap == d_up: 
                    self.camera.pos[1] = max_ey + h + 0.001
                    if self.vertical_velocity < 0: self.vertical_velocity = 0
                    self.is_grounded = True
                elif min_overlap == d_down: 
                    self.camera.pos[1] = min_ey - 0.001
                    if self.vertical_velocity > 0: self.vertical_velocity = 0
                elif min_overlap == d_left:  self.camera.pos[0] = min_ex - r - pad
                elif min_overlap == d_right: self.camera.pos[0] = max_ex + r + pad
                elif min_overlap == d_back:  self.camera.pos[2] = min_ez - r - pad
                elif min_overlap == d_front: self.camera.pos[2] = max_ez + r + pad
    def handle_left_click(self):
        ray_o, ray_d = self.get_world_ray()
        keys = self.input.get_keys()
        cands = self.get_candidates_for_ray(ray_o, ray_d, max_dist=200.0)
        d_ent, _, _ = self.scene.raycast(ray_o, ray_d, candidates=cands)
        if self.tool_mode == 'DOOR_CREATOR' and d_ent and d_ent.is_door:
             if d_ent.group_id:
                 targets = [e for e in self.scene.entities if e.group_id == d_ent.group_id]
             else:
                 targets = [d_ent]
             states_before = {e.uid: e.to_dict() for e in targets}
             for t in targets:
                 t.is_door = False
                 t.hinge_edge = -1
                 t.door_open = False
             self.door_tool_state = 'HOVER'
             self.highlighted_ent = None
             self.locked_hinge_edge = -1
             states_after = {e.uid: e.to_dict() for e in targets}
             self.scene.push_modification(states_before, states_after)
             self.show_notification("DOOR GROUP REMOVED" if len(targets) > 1 else "DOOR REMOVED")
             self.mark_scene_changed(changed_entities=targets)
             return
        if not self.creative_mode:
            if d_ent and d_ent.is_door:
                self.trigger_door_animation(d_ent)
                return
        if self.tool_mode == 'SELECT':
            if not self.creative_mode:
                return
            ent, dist, norm = self.scene.raycast(ray_o, ray_d, candidates=cands)
            is_ctrl = keys.get(sdl2.SDLK_LCTRL) or keys.get(sdl2.SDLK_RCTRL)
            if not ent:
                if not is_ctrl:
                    self.selected_entities = []
                    self.selected_faces = {}
                return
            if norm is not None:
                self.push_pull_normal = norm
            else:
                self.push_pull_normal = np.array([0.0, 1.0, 0.0])
            face_idx = self.get_face_index_from_norm(norm)
            targets = []
            if ent.group_id:
                for e in self.scene.entities:
                    if e.group_id == ent.group_id:
                        targets.append(e)
            else:
                targets = [ent]
            if is_ctrl:
                for t in targets:
                    if t not in self.selected_entities: 
                        self.selected_entities.append(t)
                if face_idx is not None:
                    if ent not in self.selected_faces: 
                        self.selected_faces[ent] = set()
                    if face_idx in self.selected_faces[ent]:
                        self.selected_faces[ent].remove(face_idx)
                        if not self.selected_faces[ent]:
                            del self.selected_faces[ent]
                            should_deselect_group = True
                            if ent.group_id:
                                group_mates = [e for e in self.selected_entities if e.group_id == ent.group_id]
                                for mate in group_mates:
                                    if mate in self.selected_faces and self.selected_faces[mate]:
                                        should_deselect_group = False
                                        break
                            else:
                                should_deselect_group = True
                            if should_deselect_group:
                                if ent.group_id:
                                    group_mates = [e for e in self.selected_entities if e.group_id == ent.group_id]
                                    for mate in group_mates:
                                        if mate in self.selected_entities:
                                            self.selected_entities.remove(mate)
                                        if mate in self.selected_faces:
                                            del self.selected_faces[mate]
                                else:
                                    if ent in self.selected_entities:
                                        self.selected_entities.remove(ent)
                    else:
                        self.selected_faces[ent].add(face_idx)
            else:
                self.selected_entities = []
                self.selected_faces = {}
                self.selected_entities.extend(targets)
                if face_idx is not None:
                    self.selected_faces[ent] = {face_idx}
            return
        elif self.tool_mode == 'WALL':
            ent, _, norm = self.scene.raycast(ray_o, ray_d, candidates=cands)
            hit = self.get_smart_cursor(ray_o, ray_d)
            if hit is not None:
                if self.build_start is None:
                    self.build_start = hit
                    if ent and norm is not None: self.build_normal = norm
                    else: self.build_normal = np.array([0.0, 1.0, 0.0])
                else:
                    self.create_wall(self.build_start, hit)
                    self.build_start = None
                    self.build_normal = None
        elif self.tool_mode == 'ROOM':
            if self.room_extruding:
                ray_o, ray_d = self.get_world_ray()
                current_h = self.calculate_extrusion_height_generic(ray_o, ray_d, self.room_base_rect)
                self.finalize_room(current_h)
                self.room_extruding = False
                self.build_start = None
                return
            hit = self.get_smart_cursor(ray_o, ray_d)
            if hit is not None:
                if self.build_start is None:
                    self.build_start = hit
                    ent, _, norm = self.scene.raycast(ray_o, ray_d, candidates=cands)
                    if ent and norm is not None: self.build_normal = norm
                    else: self.build_normal = np.array([0.0, 1.0, 0.0])
                    self.constraint_axis = np.argmax(np.abs(self.build_normal))
                else:
                    diff_vec = np.abs(hit - self.build_start)
                    if np.all(diff_vec > 0.05):
                        self.create_room_by_2_points(self.build_start, hit)
                        self.build_start = None
                        self.room_extruding = False
                    else:
                        self.room_extruding = True
                        self.room_base_rect = {'p1': self.build_start, 'p2': hit}
                        ray_o, ray_d = self.get_world_ray()
                        self.extrusion_start_val = self.calculate_extrusion_raw(ray_o, ray_d, self.room_base_rect, self.build_normal)
        elif self.tool_mode == 'BOX':
            if self.box_extruding:
                ray_o, ray_d = self.get_world_ray()
                current_h = self.calculate_extrusion_height_generic(ray_o, ray_d, self.box_base_rect)
                self.finalize_box(current_h)
                self.box_extruding = False
                self.build_start = None
                return
            hit = self.get_smart_cursor(ray_o, ray_d)
            if hit is not None:
                if self.build_start is None:
                    self.build_start = hit
                    ent, _, norm = self.scene.raycast(ray_o, ray_d, candidates=cands)
                    if ent and norm is not None: self.build_normal = norm
                    else: self.build_normal = np.array([0.0, 1.0, 0.0])
                    self.constraint_axis = np.argmax(np.abs(self.build_normal))
                else:
                    diff_vec = np.abs(hit - self.build_start)
                    if np.all(diff_vec > 0.05):
                        self.create_box_by_2_points(self.build_start, hit)
                        self.build_start = None
                        self.box_extruding = False
                    else:
                        self.box_extruding = True
                        self.box_base_rect = {'p1': self.build_start, 'p2': hit}
                        ray_o, ray_d = self.get_world_ray()
                        self.extrusion_start_val = self.calculate_extrusion_raw(ray_o, ray_d, self.box_base_rect, self.build_normal)
        elif self.tool_mode == 'STRIP':
            ray_o, ray_d = self.get_world_ray()
            now = pygame.time.get_ticks()
            if now - self.last_click_time < 200:
                if len(self.strip_points) >= 2:
                    self.strip_extruding = True
                    self.build_start = None
                    ray_o, ray_d = self.get_world_ray()
                    base_p = self.strip_points[-1]
                    self.extrusion_start_val = self.calculate_extrusion_raw(ray_o, ray_d, base_p, self.strip_normal)
                    return
            self.last_click_time = now
            if self.strip_extruding:
                if not self.strip_points: return
                base_p = self.strip_points[-1]
                ray_o, ray_d = self.get_world_ray()
                h = self.calculate_extrusion_height_generic(ray_o, ray_d, base_p)
                if abs(h) < 0.01: h = 0.1
                self.finalize_strip(h)
                self.strip_extruding = False
                self.strip_points = []
                self.build_start = None
                return
            hit = None
            if not self.strip_points:
                hit = self.get_smart_cursor(ray_o, ray_d)
                if hit is not None:
                    current_snap = 0.01 if (keys.get(sdl2.SDLK_LCTRL) or keys.get(sdl2.SDLK_RCTRL)) else self.snap_unit
                    hit = snap_vector(hit, current_snap)
                    self.strip_points.append(hit)
                    ent, _, norm = self.scene.raycast(ray_o, ray_d, candidates=cands)
                    if ent and norm is not None: self.strip_normal = norm
                    else: self.strip_normal = np.array([0.0, 1.0, 0.0])
                    self.strip_plane_p = hit
            else:
                last_p = self.strip_points[-1]
                plane_hit = self.get_point_on_plane(ray_o, ray_d, self.strip_plane_p, self.strip_normal)
                if plane_hit is not None:
                    keys = self.input.get_keys()
                    is_ctrl = keys.get(sdl2.SDLK_LCTRL) or keys.get(sdl2.SDLK_RCTRL)
                    snap_step = 0.01 if is_ctrl else self.snap_unit
                    curr = snap_vector(plane_hit, snap_step)
                    start_p = self.strip_points[0]
                    dist_to_start_raw = np.linalg.norm(curr - start_p)
                    magnet_active = (dist_to_start_raw < 0.1) and (not is_ctrl)
                    final_p = None
                    corner_p = None 
                    norm_axis = np.argmax(np.abs(self.strip_normal))
                    if magnet_active:
                        final_p = start_p
                        vec_to_start = start_p - last_p
                        vec_to_start[norm_axis] = 0
                        dom_axis = np.argmax(np.abs(vec_to_start))
                        is_diagonal = False
                        for i in range(3):
                            if i != dom_axis and i != norm_axis:
                                if abs(vec_to_start[i]) > 0.001:
                                    is_diagonal = True
                        if is_diagonal:
                            corner_p = last_p.copy()
                            corner_p[dom_axis] = start_p[dom_axis]
                    else:
                        diff = curr - last_p
                        diff[norm_axis] = 0
                        dom_axis = np.argmax(np.abs(diff))
                        final_p = last_p.copy()
                        final_p[dom_axis] = curr[dom_axis]
                    if np.linalg.norm(final_p - last_p) < 0.001:
                        if magnet_active and len(self.strip_points) >= 2:
                            self.strip_points.append(start_p) 
                            self.strip_extruding = True
                            self.build_start = None
                        return
                    if corner_p is not None:
                        self.strip_points.append(corner_p)
                    self.strip_points.append(final_p)
                    if magnet_active and len(self.strip_points) >= 3: 
                         self.strip_extruding = True
                         self.build_start = None
        elif self.tool_mode == 'CUT':
            ent, dist, norm = self.scene.raycast(ray_o, ray_d, ignore_holes=True, candidates=cands)
            keys = self.input.get_keys()
            is_alt = keys.get(sdl2.SDLK_LALT) or keys.get(sdl2.SDLK_RALT)
            is_ctrl = keys.get(sdl2.SDLK_LCTRL) or keys.get(sdl2.SDLK_RCTRL)
            current_snap = 0.01 if is_ctrl else self.snap_unit
            if self.cut_start_point is None:
                ground_hit = self.get_ground_intersect(ray_o, ray_d)
                dist_ground = np.inf
                is_over_hole = False
                if ground_hit is not None:
                    dist_ground = np.linalg.norm(ground_hit - ray_o)
                    for e in self.scene.entities:
                        if e.is_hole:
                            h_min, h_max = e.get_aabb()
                            if (h_min[0] <= ground_hit[0] <= h_max[0] and 
                                h_min[2] <= ground_hit[2] <= h_max[2]):
                                is_over_hole = True
                                break
                prioritize_ground = False
                if ground_hit is not None and not is_over_hole:
                    if ent is None:
                        prioritize_ground = True
                    elif dist_ground < dist: 
                        prioritize_ground = True
                if prioritize_ground:
                    self.cut_start_point = snap_vector(ground_hit, current_snap)
                    self.cut_target_ent = None 
                    self.cut_normal = np.array([0.0, 1.0, 0.0])
                elif ent and norm is not None:
                    hit_raw = ray_o + ray_d * dist
                    self.cut_start_point = snap_vector(hit_raw, current_snap)
                    self.cut_normal = norm
                    self.cut_target_ent = ent
            else:
                if self.cut_target_ent is not None:
                    hit_on_plane = self.get_point_on_plane(ray_o, ray_d, self.cut_start_point, self.cut_normal)
                    if hit_on_plane is not None:
                        cut_end_point = snap_vector(hit_on_plane, current_snap)
                        self.perform_multi_cut(
                            self.cut_start_point, 
                            cut_end_point, 
                            self.cut_normal, 
                            target_ent=self.cut_target_ent,
                            is_alt=is_alt
                        )
                    self.cut_start_point = None
                    self.cut_normal = None
                    self.cut_target_ent = None
                else:
                    ground_hit = self.get_ground_intersect(ray_o, ray_d)
                    if ground_hit is not None:
                        p1 = self.cut_start_point
                        p2 = snap_vector(ground_hit, current_snap)
                        p_min = np.minimum(p1, p2)
                        p_max = np.maximum(p1, p2)
                        size = p_max - p_min
                        size[1] = 0.05 
                        if size[0] < 0.01 or size[2] < 0.01:
                            self.cut_start_point = None
                            return
                        center = (p_min + p_max) / 2.0
                        center[1] = 0.0 
                        hole_ent = Entity(center, size)
                        hole_ent.is_hole = True
                        hole_ent.faces_colors = [[0,0,0,0.5]] * 6 
                        self.scene.add_entity(hole_ent)
                        self.mark_scene_changed(changed_entities=[hole_ent])
                        self.show_notification(self.tr('NOTIF_HOLE_CREATED'))
                    self.cut_start_point = None
        elif self.tool_mode == 'SLICE':
            ent, dist, norm = self.scene.raycast(ray_o, ray_d, candidates=cands)
            if ent:
                raw_hit_point = ray_o + ray_d * dist
                keys = self.input.get_keys()
                is_ctrl = keys.get(sdl2.SDLK_LCTRL) or keys.get(sdl2.SDLK_RCTRL)
                snap = 0.01 if is_ctrl else self.snap_unit
                hit_point = snap_vector(raw_hit_point, snap)
                is_alt = keys.get(sdl2.SDLK_LALT) or keys.get(sdl2.SDLK_RALT)
                slice_norm = np.array([0.0, 1.0, 0.0])
                use_cached_norm = False
                if self.last_slice_pos is not None:
                    dist_moved = np.linalg.norm(raw_hit_point - self.last_slice_pos)
                    if dist_moved < 0.02: 
                        slice_norm = self.last_slice_norm
                        use_cached_norm = True
                if not use_cached_norm:
                    is_floor = (norm is not None and abs(norm[1]) > 0.5)
                    if is_floor:
                        if self.slice_orientation == 0:
                            slice_norm = np.array([1.0, 0.0, 0.0]) 
                        else:
                            slice_norm = np.array([0.0, 0.0, 1.0]) 
                    else:
                        if self.slice_orientation == 0:
                            if norm is not None:
                                if abs(norm[0]) > 0.5: slice_norm = np.array([0.0, 0.0, 1.0])
                                elif abs(norm[2]) > 0.5: slice_norm = np.array([1.0, 0.0, 0.0])
                                else: slice_norm = np.array([0.0, 1.0, 0.0])
                        else:
                            slice_norm = np.array([0.0, 1.0, 0.0])
                self.perform_slice(hit_point, slice_norm, ent, is_alt)
    def get_smart_cursor(self, ray_o, ray_d):
        keys = self.input.get_keys()
        is_ctrl = keys.get(sdl2.SDLK_LCTRL) or keys.get(sdl2.SDLK_RCTRL)
        current_snap = 0.01 if is_ctrl else self.snap_unit
        final_point = None
        if self.build_start is not None:
            normal = np.zeros(3)
            normal[self.constraint_axis] = 1.0
            denom = np.dot(normal, ray_d)
            if abs(denom) > 1e-6:
                t = np.dot(normal, (self.build_start - ray_o)) / denom
                if t >= 0:
                    final_point = ray_o + ray_d * t
        if final_point is None:
            cands = self.get_candidates_for_ray(ray_o, ray_d)
            ent, dist, norm = self.scene.raycast(ray_o, ray_d, candidates=cands)
            if ent:
                final_point = ray_o + ray_d * dist
                final_point += norm * 0.0001
            else:
                final_point = self.get_ground_intersect(ray_o, ray_d)
        if final_point is None:
            return None
        if not is_ctrl:
            best_snap = None
            min_dist = 0.2
            for ent in self.scene.entities:
                b_min, b_max = ent.get_aabb()
                corners = [
                    np.array([b_min[0], b_min[1], b_min[2]]),
                    np.array([b_max[0], b_min[1], b_min[2]]),
                    np.array([b_max[0], b_max[1], b_min[2]]),
                    np.array([b_min[0], b_max[1], b_min[2]]),
                    np.array([b_min[0], b_min[1], b_max[2]]),
                    np.array([b_max[0], b_min[1], b_max[2]]),
                    np.array([b_max[0], b_max[1], b_max[2]]),
                    np.array([b_min[0], b_max[1], b_max[2]]),
                ]
                for c in corners:
                    d = np.linalg.norm(c - final_point)
                    if d < min_dist:
                        min_dist = d
                        best_snap = c
            if best_snap is not None:
                return best_snap
        return snap_vector(final_point, current_snap)
    def create_wall(self, start, end):
        p_min = np.minimum(start, end)
        p_max = np.maximum(start, end)
        size = p_max - p_min
        for i in range(3):
            if size[i] < 0.001: 
                size[i] = self.default_thickness
        center = p_min + size / 2.0
        if self.build_normal is not None:
            for i in range(3):
                if abs(size[i] - self.default_thickness) < 0.001:
                    if self.build_normal[i] < -0.5:
                        center[i] -= size[i]
        w = Entity(center, size)
        c = self.last_paint_settings['color']
        w.faces_colors = [list(c)] * 6
        is_tiling_val = self.last_paint_settings.get('is_tiling', False)
        w.faces_tiling = [is_tiling_val] * 6
        w.density = self.last_paint_settings.get('density', 1.0)
        refl_val = self.last_paint_settings.get('reflectivity', 0.0)
        w.faces_reflectivity = [refl_val] * 6
        tex = self.last_paint_settings.get('texture_path', None)
        if tex:
            w.faces_textures = [tex] * 6
            self.texture_manager.load_from_file(tex)
        self.scene.add_entity(w)
        self.mark_scene_changed(changed_entities=[w])
    def finalize_room(self, extrusion_val):
        p1 = self.room_base_rect['p1']
        p2 = self.room_base_rect['p2']
        p_min = np.minimum(p1, p2)
        p_max = np.maximum(p1, p2)
        size = p_max - p_min
        axis = self.constraint_axis
        base_center = (p_min + p_max) / 2.0
        final_center = base_center.copy()
        final_center[axis] += extrusion_val / 2.0
        final_size = size.copy()
        final_size[axis] = abs(extrusion_val)
        final_center, final_size = snap_bounds_to_grid_3d(final_center, final_size, precision=0.01)
        self._build_room_geometry(final_center, final_size, color=self.last_paint_settings['color'])
    def _build_room_geometry(self, center, size, color=None):
        gid = None   
        thickness = self.default_thickness
        y_bottom = center[1] - size[1]/2
        y_top = center[1] + size[1]/2
        floor = Entity([center[0], y_bottom + thickness/2, center[2]], [size[0], thickness, size[2]], gid)
        ceil = Entity([center[0], y_top - thickness/2, center[2]], [size[0], thickness, size[2]], gid)
        h_wall = size[1]
        y_wall = center[1]
        w1 = Entity([center[0], y_wall, center[2] - size[2]/2 + thickness/2], [size[0], h_wall, thickness], gid)
        w2 = Entity([center[0], y_wall, center[2] + size[2]/2 - thickness/2], [size[0], h_wall, thickness], gid)
        w3 = Entity([center[0] - size[0]/2 + thickness/2, y_wall, center[2]], [thickness, h_wall, size[2]], gid)
        w4 = Entity([center[0] + size[0]/2 - thickness/2, y_wall, center[2]], [thickness, h_wall, size[2]], gid)
        base_col = list(color) if color else [1.0, 1.0, 1.0, 1.0, 0.0, 0.0]
        is_tiling_val = self.last_paint_settings.get('is_tiling', False)
        density_val = self.last_paint_settings.get('density', 1.0)
        refl_val = self.last_paint_settings.get('reflectivity', 0.0) 
        tex_path = self.last_paint_settings.get('texture_path', None)
        if tex_path:
            self.texture_manager.load_from_file(tex_path)
        new_entities = [floor, ceil, w1, w2, w3, w4]
        for e in new_entities:
            e.faces_colors = [base_col] * 6
            e.faces_tiling = [is_tiling_val] * 6
            e.density = density_val
            e.faces_reflectivity = [refl_val] * 6
            if tex_path:
                e.faces_textures = [tex_path] * 6
            self.scene.entities.append(e)
        self.scene.push_transaction(
            added_ents=new_entities, 
            removed_ents=[], 
            modified_triplets=[]
        )
        self.mark_scene_changed(changed_entities=new_entities)
    def perform_multi_cut(self, p1, p2, normal, target_ent=None, is_alt=False): 
        axis = np.argmax(np.abs(normal))
        targets = []
        if is_alt and self.selected_entities:
            targets = list(self.selected_entities)
        elif target_ent:
            if is_alt: targets = self.find_connected_entities(target_ent)
            else: targets = ([e for e in self.scene.entities if e.group_id == target_ent.group_id] if target_ent.group_id else [target_ent])
        else:
            plane_coord = p1[axis]
            for ent in self.scene.entities:
                half = ent.scale[axis]/2.0
                if ent.pos[axis]-half-0.001 <= plane_coord <= ent.pos[axis]+half+0.001: targets.append(ent)
        if not targets: return
        u_axis = (axis + 1) % 3
        v_axis = (axis + 2) % 3
        cut_u_min = min(p1[u_axis], p2[u_axis]); cut_u_max = max(p1[u_axis], p2[u_axis])
        cut_v_min = min(p1[v_axis], p2[v_axis]); cut_v_max = max(p1[v_axis], p2[v_axis])
        transaction_added = []; transaction_removed = []; visual_updates = []
        for ent in targets:
            half = ent.scale / 2.0
            ent_u_min = ent.pos[u_axis] - half[u_axis]; ent_u_max = ent.pos[u_axis] + half[u_axis]
            ent_v_min = ent.pos[v_axis] - half[v_axis]; ent_v_max = ent.pos[v_axis] + half[v_axis]
            if (cut_u_max <= ent_u_min or cut_u_min >= ent_u_max or cut_v_max <= ent_v_min or cut_v_min >= ent_v_max): continue
            hole_u_min = max(cut_u_min, ent_u_min); hole_u_max = min(cut_u_max, ent_u_max)
            hole_v_min = max(cut_v_min, ent_v_min); hole_v_max = min(cut_v_max, ent_v_max)
            if (hole_u_max - hole_u_min < 0.009) or (hole_v_max - hole_v_min < 0.009): continue
            new_parts = []
            def add_block(u_start, u_end, v_start, v_end):
                w = u_end - u_start
                h = v_end - v_start
                if w < 0.001 or h < 0.001: return
                new_pos = np.zeros(3)
                new_pos[axis] = ent.pos[axis]
                new_pos[u_axis] = u_start + w/2.0
                new_pos[v_axis] = v_start + h/2.0
                new_scale = np.zeros(3)
                new_scale[axis] = ent.scale[axis]
                new_scale[u_axis] = w
                new_scale[v_axis] = h
                new_part = Entity(
                    pos=new_pos, scale=new_scale, group_id=ent.group_id, color=None,
                    group_history=list(ent.group_history),
                    faces_colors=copy.deepcopy(ent.faces_colors),
                    faces_textures=list(ent.faces_textures),
                    faces_uv_data=copy.deepcopy(ent.faces_uv_data)
                )
                new_part.faces_tiling = copy.deepcopy(ent.faces_tiling)
                new_part.density = ent.density
                new_part.faces_reflectivity = list(ent.faces_reflectivity)
                TextureUtils.preserve_texture_pos(ent, new_part)
                new_parts.append(new_part)
            add_block(ent_u_min, hole_u_min, ent_v_min, ent_v_max) 
            add_block(hole_u_max, ent_u_max, ent_v_min, ent_v_max) 
            add_block(hole_u_min, hole_u_max, ent_v_min, hole_v_min) 
            add_block(hole_u_min, hole_u_max, hole_v_max, ent_v_max) 
            if ent in self.scene.entities: self.scene.entities.remove(ent)
            self.scene.entities.extend(new_parts)
            transaction_removed.append(ent)
            transaction_added.extend(new_parts)
            if ent in self.selected_entities:
                self.selected_entities.remove(ent)
                self.selected_entities.extend(new_parts)
                if ent in self.selected_faces: del self.selected_faces[ent]
            visual_updates.append(ent)
            visual_updates.extend(new_parts)
        if transaction_removed:
            self.scene.push_transaction(transaction_added, transaction_removed, [])
            self.mark_scene_changed(changed_entities=visual_updates)
    def io_save(self):
        if self.current_filename:
            return self._perform_save(self.current_filename)
        self.set_mouse_lock(False)
        self.file_dialog.open('save', self.on_file_dialog_result)
        return True
    def io_load(self):
        self.set_mouse_lock(False)
        self.file_dialog.open('load', self.on_file_dialog_result)
    def on_file_dialog_result(self, filename):
        if filename is None:
            # Если отменили диалог, возвращаем мышь, если мы в игровом режиме
            if self.state in ["GAME", "CINECAM", "SUN_SETTINGS"]:
                self.set_mouse_lock(True)
            return
        if self.file_dialog.mode == 'save' and self.file_dialog.is_exporting:
            self.show_notification(self.tr('NOTIF_EXPORT'))
            sdl2.SDL_PumpEvents() 
            success = ExportManager.export_scene(filename, self.scene, self.texture_manager, self.CHUNK_SIZE)
            if success:
                self.show_notification(self.tr('NOTIF_EXPORT_OK').format(name=os.path.basename(filename)))
            if self.state == "GAME" or self.state == "SUN_SETTINGS" or self.state == "CINECAM":
                self.set_mouse_lock(True)
            else:
                self.set_mouse_lock(False)
            return
        if self.file_dialog.mode == 'save':
            self.current_filename = filename
            self._perform_save(filename)
        elif self.file_dialog.mode == 'load':
            # --- ИСПРАВЛЕНИЕ: Полная очистка GPU-кешей перед загрузкой ---
            # Это удаляет "призраков" из предыдущего мира
            for mesh_dict in self.chunk_meshes.values():
                for mesh in mesh_dict.values():
                    mesh.delete()
            self.chunk_meshes.clear()
            self.compiled_chunks.clear()
            
            for mesh_dict in self.large_objects_gl_cache.values():
                for mesh in mesh_dict.values():
                    mesh.delete()
            self.large_objects_gl_cache.clear()
            self.cached_large_entities = []
            # -----------------------------------------------------------

            try:
                self.current_filename = filename
                scene_data = None
                is_zip = zipfile.is_zipfile(filename)
                if is_zip:
                    with zipfile.ZipFile(filename, 'r') as zf:
                        with zf.open("scene.json") as f:
                            scene_data = json.load(f)
                        for member in zf.namelist():
                            if member.startswith("textures/") and not member.endswith("/"):
                                file_data = zf.read(member)
                                file_io = io.BytesIO(file_data)
                                self.texture_manager.load_from_memory(member, file_io)
                else:
                    with open(filename, 'r') as f:
                        scene_data = json.load(f)
                self.scene.undo_stack = []
                self.scene.redo_stack = []
                self.scene.entities = [Entity.from_dict(d) for d in scene_data['entities']]
                self.cached_large_entities = [e for e in self.scene.entities if max(e.scale) > self.CHUNK_SIZE]
                self.compile_large_entities()
                for ent in self.scene.entities:
                     ent.pos, ent.scale = snap_bounds_to_grid_3d(ent.pos, ent.scale, precision=0.01)
                if "player" in scene_data:
                    p = scene_data["player"]
                    self.camera.pos = np.array(p["pos"], dtype=np.float32)
                    self.camera.yaw = p["yaw"]
                    self.camera.pitch = p["pitch"]
                    self.camera.visual_y = self.camera.pos[1]
                    self.camera.update_vectors()
                    self.lantern_radius = p.get("lantern_radius", 15.0)
                    loaded_creative = p.get("creative_mode", True)
                    loaded_fly_speed = p.get("fly_speed", 5.0)
                    self.creative_mode = loaded_creative
                    if self.creative_mode:
                        self.camera.speed = loaded_fly_speed
                        self.tool_mode = 'SELECT'
                        self.edit_mode = False
                        self.current_sky_color = COLOR_SKY
                    else:
                        self.saved_creative_speed = loaded_fly_speed
                        self.camera.speed = self.fixed_adventure_speed
                        self.tool_mode = 'SELECT'
                        self.edit_mode = True
                        self.selected_entities = []
                        self.player_height = self.stand_height
                        self.vertical_velocity = 0.0
                if "environment" in scene_data:
                    env = scene_data["environment"]
                    self.sun_angle_time = env.get("sun_time", 90.0)
                    self.sun_rotation_y = env.get("sun_rotation", 0.0)
                    self.sun_speed = env.get("sun_speed", 0.25)
                if "color_history" in scene_data:
                    self.color_picker.history = scene_data["color_history"]
                    self.color_picker._update_history_text_cache()
                if "settings" in scene_data:
                    settings = scene_data["settings"]
                    if "default_thickness" in settings: self.default_thickness = float(settings["default_thickness"])
                    if "fog_distance" in settings: self.fog_distance = float(settings["fog_distance"])
                    if "limit_fps" in settings:
                        self.limit_fps = settings["limit_fps"]
                        sdl2.SDL_GL_SetSwapInterval(1 if self.limit_fps else 0)
                    self.create_ui()
                if "cine_cam" in scene_data:
                    self.cine_cam.from_dict(scene_data["cine_cam"])
                else:
                    # Если в файле нет камер, сбрасываем менеджер (на всякий случай)
                    self.cine_cam = CameraManager(self)
                self.mark_scene_changed()
                self.unsaved_changes = False
                self.project_active = True
                if self.state == "MENU":
                    self.set_state("GAME")
            except Exception as e:
                print(f"Error loading: {e}")
                
                traceback.print_exc()
        self.file_dialog.active = False 
        if self.state in ["GAME", "CINECAM", "SUN_SETTINGS"]:
            self.set_mouse_lock(True)
            sdl2.SDL_SetRelativeMouseMode(sdl2.SDL_TRUE)
            sdl2.SDL_ShowCursor(sdl2.SDL_DISABLE)
    def _perform_save(self, filename):
        try:
            snapped_entities = []
            for ent in self.scene.entities:
                clean_pos, clean_scale = snap_bounds_to_grid_3d(ent.pos, ent.scale, precision=0.01)
                if (np.linalg.norm(ent.pos - clean_pos) > 0.0001 or 
                    np.linalg.norm(ent.scale - clean_scale) > 0.0001):
                    ent.pos = clean_pos
                    ent.scale = clean_scale
                    snapped_entities.append(ent)
            save_speed = self.camera.speed if self.creative_mode else self.saved_creative_speed
            used_textures = set()
            for ent in self.scene.entities:
                for tex_path in ent.faces_textures:
                    if tex_path:
                        used_textures.add(tex_path)
            texture_mapping = {} 
            archive_texture_files = {} 
            for i, path in enumerate(used_textures):
                ext = os.path.splitext(path)[1]
                if not ext: ext = ".png"
                archive_name = f"textures/tex_{i}{ext}"
                texture_mapping[path] = archive_name
                archive_texture_files[archive_name] = path
            entities_data = []
            for ent in self.scene.entities:
                d = ent.to_dict()
                new_textures = []
                for t in d['faces_textures']:
                    if t in texture_mapping:
                        new_textures.append(texture_mapping[t])
                    else:
                        new_textures.append(None)
                d['faces_textures'] = new_textures
                entities_data.append(d)
            scene_data = {
                "version": "2",  
                "player": {
                    "pos": self.camera.pos.tolist(),
                    "yaw": self.camera.yaw,
                    "pitch": self.camera.pitch,
                    "lantern_radius": self.lantern_radius,
                    "creative_mode": self.creative_mode,
                    "fly_speed": save_speed
                },
                "environment": {
                    "sun_time": self.sun_angle_time,
                    "sun_rotation": self.sun_rotation_y,
                    "sun_speed": self.sun_speed
                },
                "entities": entities_data,
                "color_history": self.color_picker.history,
                
                # --- ДОБАВЛЕНО: Сохранение камер ---
                "cine_cam": self.cine_cam.to_dict(),
                # -----------------------------------
                
                "settings": {
                    "default_thickness": self.default_thickness,
                    "fog_distance": self.fog_distance,
                    "limit_fps": self.limit_fps
                }
            }
            if not filename.endswith('.ant') and not filename.endswith('.zip'):
                filename += '.ant'
            class NumpyEncoder(json.JSONEncoder):
                def default(self, obj):
                    if isinstance(obj, np.integer):
                        return int(obj)
                    if isinstance(obj, np.floating):
                        return float(obj)
                    if isinstance(obj, np.ndarray):
                        return obj.tolist()
                    return super(NumpyEncoder, self).default(obj)
            with zipfile.ZipFile(filename, 'w', zipfile.ZIP_DEFLATED) as zf:
                json_str = json.dumps(scene_data, indent=2, cls=NumpyEncoder)
                zf.writestr("scene.json", json_str)
                for arc_name, real_path in archive_texture_files.items():
                    try:
                        if os.path.exists(real_path):
                            zf.write(real_path, arc_name)
                        else:
                            print(f"Warning: Texture file not found for saving: {real_path}")
                    except Exception as e:
                        print(f"Error packing texture {real_path}: {e}")
            if snapped_entities:
                self.mark_scene_changed(changed_entities=snapped_entities)
            self.unsaved_changes = False
            self.show_notification(self.tr('NOTIF_SAVED'))
            if self.state == "CONFIRM_SAVE" and self.pending_exit_action:
                self.finalize_action()
            return True
        except Exception as e:
            print(f"Error saving: {e}")
            
            traceback.print_exc()
            return False
    def _reset_project(self):
        self.scene.clear()
        self.current_filename = None
        self.project_active = True
        
        # СБРОС ВСЕХ ПАРАМЕТРОВ
        self._reset_simulation_state()
        
        self.set_state("GAME")
        
        # Очистка кешей рендера
        for mesh_dict in self.chunk_meshes.values():
            for mesh in mesh_dict.values():
                mesh.delete()
        self.chunk_meshes.clear()
        self.compiled_chunks.clear()
        
        for mesh_dict in self.large_objects_gl_cache.values():
            for mesh in mesh_dict.values():
                mesh.delete()
        self.large_objects_gl_cache.clear()
        self.cached_large_entities = []
        
        self.mark_scene_changed()
        self.unsaved_changes = False
    def _reset_simulation_state(self):
        # --- Сброс окружения (Солнце и Небо) ---
        self.sun_angle_time = 90.0
        self.sun_angle_tilt = 20.0
        self.sun_rotation_y = 0.0
        self.sun_speed = 0.25
        self.day_time = 0.5
        self.current_sky_color = COLOR_SKY
        self.ambient_light = np.array([0.2, 0.2, 0.2], dtype=np.float32)
        self.light_intensity = 1.0
        self.light_dir = np.array([0.0, 1.0, 0.0], dtype=np.float32)
        self.light_color = np.array([1.0, 1.0, 1.0], dtype=np.float32)

        # --- Сброс игрока и режимов ---
        self.creative_mode = True
        self.camera = Camera() # Создаем новую камеру (сброс позиции и угла)
        self.camera.speed = 5.0
        self.vertical_velocity = 0.0
        self.player_height = 1.8
        self.lantern_radius = 15.0
        self.last_stable_pos = np.array([0.0, 1.8, 0.0], dtype=np.float32)

        # --- Сброс инструментов ---
        self.tool_mode = 'SELECT'
        self.manipulation_mode = 'MOVE'
        self.edit_mode = False
        self.selected_entities = []
        self.selected_faces = {}
        self.highlighted_ent = None
        self.build_start = None
        self.cut_start_point = None
        self.room_extruding = False
        self.box_extruding = False
        self.strip_points = []
        self.strip_extruding = False
        self.door_tool_state = 'HOVER'
        self.door_animations = []
        
        # --- Сброс Кино-камеры ---
        self.cine_cam = CameraManager(self)
        
        # --- Сброс истории текстур ---
        self.local_tex_history = []
        self.local_tex_history_idx = -1
        self.tex_session_active = False
    def _draw_button_bg(self, btn):
        col = (0.3, 0.3, 0.3, 0.8) if btn.hovered else (0.2, 0.2, 0.2, 0.8)
        self.solid_renderer.add_quad_2d(btn.rect.x, btn.rect.y, btn.rect.w, btn.rect.h, col)
    def _draw_button_text(self, btn, proj):
        if hasattr(btn, 'tex') and btn.tex:
            tx = btn.rect.x + (btn.rect.w - btn.tw) // 2
            ty = btn.rect.y + (btn.rect.h - btn.th) // 2
            self.sprite_renderer.draw_ui_sprite(btn.tex, tx, ty, btn.tw, btn.th, proj)
    def quick_save(self):
        if self.current_filename:
            self._perform_save(self.current_filename)
        else:
            self.io_save() 
    def render_ui(self):
        width, height = self.win_w, self.win_h
        ui_proj = MatrixUtils.ortho_2d(0, width, height, 0)
        if self.is_rendering_video: return
        glDisable(GL_DEPTH_TEST)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        if self.state == "CINECAM":
            self.cine_cam.draw_ui(ui_proj)
            # Рисуем перекрестие
            cx, cy = width // 2, height // 2
            self.line_renderer.add_line([cx-10, cy, 0], [cx+10, cy, 0], (1,1,1,1))
            self.line_renderer.add_line([cx, cy-10, 0], [cx, cy+10, 0], (1,1,1,1))
            self.line_renderer.flush(MatrixUtils.identity(), ui_proj)
            # Возвращаемся, чтобы не рисовать стандартный UI игры
            if hasattr(self, 'file_dialog') and self.file_dialog.active:
                pass 
            else:
                return 
        if self.state == "GAME" or self.state == "SUN_SETTINGS":
            cx, cy = width // 2, height // 2
            self.line_renderer.add_line([cx-10, cy, 0], [cx+10, cy, 0], (1,1,1,1))
            self.line_renderer.add_line([cx, cy-10, 0], [cx, cy+10, 0], (1,1,1,1))
            self.line_renderer.flush(MatrixUtils.identity(), ui_proj) 
            if self.creative_mode and self.rect_selecting:
                x1, y1 = self.rect_start
                x2, y2 = self.rect_current
                if x2 > x1: 
                    col_fill = (0.0, 0.0, 1.0, 0.2)
                    col_border = (0.0, 0.0, 1.0, 0.8)
                else: 
                    col_fill = (0.0, 1.0, 0.0, 0.2)
                    col_border = (0.0, 1.0, 0.0, 0.8)
                min_x = min(x1, x2)
                min_y = min(y1, y2)
                w = abs(x2 - x1)
                h = abs(y2 - y1)
                self.solid_renderer.add_quad_2d(min_x, min_y, w, h, col_fill)
                self.solid_renderer.flush(MatrixUtils.identity(), ui_proj)
                p1 = [min_x, min_y, 0]
                p2 = [min_x + w, min_y, 0]
                p3 = [min_x + w, min_y + h, 0]
                p4 = [min_x, min_y + h, 0]
                self.line_renderer.add_line(p1, p2, col_border)
                self.line_renderer.add_line(p2, p3, col_border)
                self.line_renderer.add_line(p3, p4, col_border)
                self.line_renderer.add_line(p4, p1, col_border)
                self.line_renderer.flush(MatrixUtils.identity(), ui_proj)
            if self.creative_mode:
                raw_scale = height / 700.0
                scale = max(1.2, min(1.8, raw_scale))
                self.color_picker.update_position(width - int(320 * scale) - 20, int(20 * scale), height)
            if self.creative_mode or self.state == "SUN_SETTINGS":
                tool_text = ""
                snap_text = ""
                hint_text = ""
                if self.state == "SUN_SETTINGS":
                    tool_text = f"{self.tr('TOOL')}: {self.tr('SUN_EDITOR')}"
                    display_speed = self.sun_speed * 10.0
                    if abs(display_speed) < 0.1: display_speed = 0.0
                    # Используем формат из словаря
                    snap_text = self.tr('SUN_INFO').format(
                        time=int(self.sun_angle_time), 
                        rot=int(self.sun_rotation_y), 
                        speed=display_speed
                    )
                    hint_text = self.tr('HINT_SUN')
                else:
                    axis_char = "Y"
                    if self.transform_axis == 0: axis_char = "X"
                    elif self.transform_axis == 2: axis_char = "Z"
                    axis_info = f"{axis_char}"
                    if self.transform_axis == 1: axis_info += f" ({self.tr('VERT')})"
                    
                    if self.tool_mode == 'SELECT':
                        # Переводим режим манипуляции (MOVE/RESIZE) через функцию tr()
                        mode_str = self.tr(self.manipulation_mode) 
                        tool_text = f"{self.tr('TOOL')}: {self.tr('SELECT')} [{mode_str}]  |  {self.tr('AXIS')}: {axis_info}"
                    elif self.tool_mode == 'CUBE':
                        tool_text = f"{self.tr('TOOL')}: {self.tr('CUBE')}"
                        snap_text = self.tr('HINT_CUBE')
                    else:
                        tool_text = f"{self.tr('TOOL')}: {self.tr(self.tool_mode)}" # Убедитесь что ключи WALL, BOX совпадают с tool_mode
                        if self.build_start is not None:
                            cstr_char = "Y"
                            if self.constraint_axis == 0: cstr_char = "X"
                            elif self.constraint_axis == 2: cstr_char = "Z"
                            tool_text += f" | {self.tr('CONSTR')}: {cstr_char}"
                        elif self.tool_mode == 'SLICE':
                            orient = self.tr('VERTICAL') if self.slice_orientation == 0 else self.tr('HORIZONTAL')
                            tool_text += f" | {self.tr('MODE')}: {orient}"
                            
                    if self.tool_mode != 'CUBE': # Для куба свой snap_text
                        snap_text = f"{self.tr('SNAP')}: {self.snap_unit}m"
                        
                    hint_text = self.tr('HINT_GAME')
                self.lbl_tool.set_text(tool_text)
                self.lbl_snap.set_text(snap_text)
                self.lbl_hint.set_text(hint_text)
                ui_scale = height / 900.0
                margin = int(10 * ui_scale)
                if self.lbl_hint.tex: self.sprite_renderer.draw_ui_sprite(self.lbl_hint.tex, (width - self.lbl_hint.w)//2, height - self.lbl_hint.h - margin, self.lbl_hint.w, self.lbl_hint.h, ui_proj)
                if self.lbl_snap.tex: self.sprite_renderer.draw_ui_sprite(self.lbl_snap.tex, (width - self.lbl_snap.w)//2, height - self.lbl_hint.h - self.lbl_snap.h - margin*2, self.lbl_snap.w, self.lbl_snap.h, ui_proj)
                if self.lbl_tool.tex: self.sprite_renderer.draw_ui_sprite(self.lbl_tool.tex, (width - self.lbl_tool.w)//2, height - self.lbl_hint.h - self.lbl_snap.h - self.lbl_tool.h - margin*3, self.lbl_tool.w, self.lbl_tool.h, ui_proj)
            self.fps_timer += 1
            if self.fps_timer > 30:
                self.lbl_fps.set_text(f"FPS: {int(self.clock.get_fps())}")
                self.fps_timer = 0
            if self.lbl_fps.tex:
                padding_right = 10
                fps_x = width - self.lbl_fps.w - padding_right
                self.sprite_renderer.draw_ui_sprite(self.lbl_fps.tex, fps_x, 10, self.lbl_fps.w, self.lbl_fps.h, ui_proj)
            now = pygame.time.get_ticks()
            if now - self.notification_timer < 2000 and self.notification_text:
                 self.solid_renderer.add_quad_2d(0, 0, width, 40, (0.0, 0.5, 0.0, 0.8))
                 self.solid_renderer.flush(MatrixUtils.identity(), ui_proj)
                 notif_lbl = TextLabel(self.font)
                 notif_lbl.set_text(self.notification_text)
                 self.sprite_renderer.draw_ui_sprite(notif_lbl.tex, (width - notif_lbl.w)//2, (40 - notif_lbl.h)//2, notif_lbl.w, notif_lbl.h, ui_proj)
                 notif_lbl.delete()
        elif self.state in ["MENU", "PAUSE", "CONFIRM_SAVE"]:
             self.solid_renderer.add_quad_2d(0, 0, width, height, (0, 0, 0, 0.7))
             if self.state == "MENU":
                 if self.project_active: self._draw_button_bg(self.btn_main_resume)
                 self._draw_button_bg(self.btn_main_new)
                 self._draw_button_bg(self.btn_load_menu)
                 self._draw_button_bg(self.btn_lang_menu) # <---
                 self._draw_button_bg(self.btn_quit_menu)
             elif self.state == "PAUSE":
                 self._draw_button_bg(self.btn_resume)
                 self._draw_button_bg(self.btn_fps)
                 self._draw_button_bg(self.btn_save)
                 self._draw_button_bg(self.btn_export)
                 self._draw_button_bg(self.btn_load)
                 self._draw_button_bg(self.btn_clear)
                 self._draw_button_bg(self.btn_menu)
                 self._draw_button_bg(self.btn_quit)
                 for sl in [self.slider_fog, self.slider_thick]:
                     self.solid_renderer.add_quad_2d(sl.rect.x, sl.rect.y, sl.rect.w, sl.rect.h, (0.3, 0.3, 0.3, 1.0))
                     ratio = (sl.value - sl.min_val) / (sl.max_val - sl.min_val)
                     kx = sl.rect.x + ratio * sl.rect.w - 5
                     k_col = (0.8, 0.8, 0.9, 1.0) if sl.hovered or sl.dragging else (0.6, 0.6, 0.7, 1.0)
                     self.solid_renderer.add_quad_2d(kx, sl.rect.y, 10, sl.rect.h, k_col)
             elif self.state == "CONFIRM_SAVE":
                 self._draw_button_bg(self.btn_confirm_yes)
                 self._draw_button_bg(self.btn_confirm_no)
                 self._draw_button_bg(self.btn_confirm_cancel)
             self.solid_renderer.flush(MatrixUtils.identity(), ui_proj)
             if self.state == "MENU":
                 if self.project_active: self._draw_button_text(self.btn_main_resume, ui_proj)
                 self._draw_button_text(self.btn_main_new, ui_proj)
                 self._draw_button_text(self.btn_load_menu, ui_proj)
                 self._draw_button_text(self.btn_lang_menu, ui_proj) # <---
                 self._draw_button_text(self.btn_quit_menu, ui_proj)
                 tx = (width - self.tw_menu)//2
                 self.sprite_renderer.draw_ui_sprite(self.tex_title_menu, tx, 100, self.tw_menu, self.th_menu, ui_proj)
             elif self.state == "PAUSE":
                 self._draw_button_text(self.btn_resume, ui_proj)
                 self._draw_button_text(self.btn_fps, ui_proj)
                 self._draw_button_text(self.btn_save, ui_proj)
                 self._draw_button_text(self.btn_export, ui_proj)
                 self._draw_button_text(self.btn_load, ui_proj)
                 self._draw_button_text(self.btn_clear, ui_proj)
                 self._draw_button_text(self.btn_menu, ui_proj)
                 self._draw_button_text(self.btn_quit, ui_proj)
                 self._draw_button_text(self.slider_fog, ui_proj)
                 self._draw_button_text(self.slider_thick, ui_proj)
                 tx = (width - self.tw_pause)//2
                 self.sprite_renderer.draw_ui_sprite(self.tex_title_pause, tx, 20, self.tw_pause, self.th_pause, ui_proj)
             elif self.state == "CONFIRM_SAVE":
                 if self.lbl_confirm_question.tex:
                    self.sprite_renderer.draw_ui_sprite(self.lbl_confirm_question.tex, (width-self.lbl_confirm_question.w)//2, height//2 - 250, self.lbl_confirm_question.w, self.lbl_confirm_question.h, ui_proj)
                 self._draw_button_text(self.btn_confirm_yes, ui_proj)
                 self._draw_button_text(self.btn_confirm_no, ui_proj)
                 self._draw_button_text(self.btn_confirm_cancel, ui_proj)
        if self.labels_to_draw_queue:
            glBindTexture(GL_TEXTURE_2D, 0)
            current_fps_w = self.lbl_fps.w if self.lbl_fps.tex else 100
            fps_zone_x = width - current_fps_w - 20 
            fps_zone_y = 40
            for label_obj, x, y in self.labels_to_draw_queue:
                draw_x, draw_y = x, y
                if draw_x > fps_zone_x and draw_y < fps_zone_y: 
                    draw_y += 40
                if label_obj.tex:
                    self.sprite_renderer.draw_ui_sprite(label_obj.tex, draw_x, draw_y, label_obj.w, label_obj.h, ui_proj)
        should_use_legacy = False
        if hasattr(self, 'file_dialog') and self.file_dialog.active:
            should_use_legacy = True
        elif self.state == "GAME" and self.creative_mode and self.color_picker.active:
            should_use_legacy = True
        if should_use_legacy:
            glUseProgram(0)
            glBindVertexArray(0)
            glBindBuffer(GL_ARRAY_BUFFER, 0)
            glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, 0)
            glEnable(GL_BLEND)
            glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
            glDisable(GL_CULL_FACE)
            glMatrixMode(GL_PROJECTION)
            glPushMatrix()
            glLoadIdentity()
            glOrtho(0, width, height, 0, -1, 1)
            glMatrixMode(GL_MODELVIEW)
            glPushMatrix()
            glLoadIdentity()
            if hasattr(self, 'file_dialog') and self.file_dialog.active:
                self.file_dialog.draw()
            elif self.color_picker.active:
                self.color_picker.draw()
            glMatrixMode(GL_MODELVIEW)
            glPopMatrix()
            glMatrixMode(GL_PROJECTION)
            glPopMatrix()
            glBindTexture(GL_TEXTURE_2D, 0)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_CULL_FACE)
    def process_sdl_event(self, event):
        # --- 1. ПРИОРИТЕТ: Файловый диалог (Меню) ---
        if hasattr(self, 'file_dialog') and self.file_dialog.active:
            if event.type == sdl2.SDL_TEXTINPUT:
                input_char = event.text.text.decode('utf-8')
                self.file_dialog.process_text_input(input_char)
            else:
                self.file_dialog.handle_event(event)
            return # Блок живого обновления удален
        # ---------------------------------------------

        # --- 2. CINE CAM: Перехват событий ---
        if self.state == "CINECAM":
            if self.cine_cam.handle_input(event):
                return
            
            # Выход по ESC
            if event.type == sdl2.SDL_KEYDOWN and event.key.keysym.sym == sdl2.SDLK_ESCAPE:
                self.set_state("GAME")
                self.show_notification(self.tr('NOTIF_CINE_OFF'))
                return
        if event.type == sdl2.SDL_MOUSEMOTION:
            mx, my = event.motion.x, event.motion.y 
            if self.state == "GAME" and self.creative_mode and self.color_picker.active:
                self.color_picker.handle_event(event, None) 
            if self.state == "PAUSE":
                self.slider_fog.handle_event(event)
                self.slider_thick.handle_event(event)
            if self.state == "GAME" and self.rect_selecting:
                self.rect_current = (event.motion.x, event.motion.y)
            if self.state == "MENU":
                if self.project_active: self.btn_main_resume.check_hover(mx, my)
                self.btn_main_new.check_hover(mx, my)
                self.btn_load_menu.check_hover(mx, my)
                self.btn_lang_menu.check_hover(mx, my) # <---
                self.btn_quit_menu.check_hover(mx, my)
            elif self.state == "PAUSE":
                self.btn_resume.check_hover(mx, my)
                self.btn_fps.check_hover(mx, my)
                self.btn_save.check_hover(mx, my)
                self.btn_export.check_hover(mx, my)
                self.btn_load.check_hover(mx, my)
                self.btn_clear.check_hover(mx, my)
                self.btn_menu.check_hover(mx, my)
                self.btn_quit.check_hover(mx, my)
            elif self.state == "CONFIRM_SAVE":
                self.btn_confirm_yes.check_hover(mx, my)
                self.btn_confirm_no.check_hover(mx, my)
                self.btn_confirm_cancel.check_hover(mx, my)
        elif event.type == sdl2.SDL_MOUSEBUTTONDOWN:
            btn = event.button.button
            mx, my = event.button.x, event.button.y
            if self.state == "MENU" and btn == sdl2.SDL_BUTTON_LEFT:
                if self.project_active and self.btn_main_resume.check_hover(mx, my): self.btn_main_resume.click()
                if self.btn_main_new.check_hover(mx, my): self.btn_main_new.click()
                if self.btn_load_menu.check_hover(mx, my): self.btn_load_menu.click()
                if self.btn_lang_menu.check_hover(mx, my): self.btn_lang_menu.click()
                if self.btn_quit_menu.check_hover(mx, my): self.btn_quit_menu.click()
            elif self.state == "PAUSE" and btn == sdl2.SDL_BUTTON_LEFT:
                if self.slider_fog.handle_event(event): pass
                elif self.slider_thick.handle_event(event): pass
                elif self.btn_resume.check_hover(mx, my): self.btn_resume.click()
                elif self.btn_fps.check_hover(mx, my): self.btn_fps.click()
                elif self.btn_save.check_hover(mx, my): self.btn_save.click()
                elif self.btn_export.check_hover(mx, my): self.btn_export.click()
                elif self.btn_load.check_hover(mx, my): self.btn_load.click()
                elif self.btn_clear.check_hover(mx, my): self.btn_clear.click()
                elif self.btn_menu.check_hover(mx, my): self.btn_menu.click()
                elif self.btn_quit.check_hover(mx, my): self.btn_quit.click()
            elif self.state == "CONFIRM_SAVE" and btn == sdl2.SDL_BUTTON_LEFT:
                if self.btn_confirm_yes.check_hover(mx, my): self.btn_confirm_yes.click()
                if self.btn_confirm_no.check_hover(mx, my): self.btn_confirm_no.click()
                if self.btn_confirm_cancel.check_hover(mx, my): self.btn_confirm_cancel.click()
            elif self.state == "GAME":
                if self.creative_mode and self.color_picker.active:
                    handled = self.color_picker.handle_event(event, self.open_texture_dialog)
                    if handled and event.type == sdl2.SDL_MOUSEBUTTONDOWN:
                        self._apply_live_ui_changes()
                    if not handled:
                        self.close_color_picker(apply=False)
                    return
                if self.mouse_locked:
                    if btn == sdl2.SDL_BUTTON_LEFT:
                        if self.tool_mode == 'CUBE':
                            # ЛКМ = ВЫРЕЗАНИЕ
                            ray_o, ray_d = self.get_world_ray()
                            # Теперь распаковываем 4 значения
                            size, center, _, _ = self._get_cube_tool_data(ray_o, ray_d, is_cutting=True)
                            if center is not None:
                                self.perform_cube_cut(center, size)
                        # ------------------------------------------
                        else:
                            self.handle_left_click() # Старая логика других инструментов
                            if self.tool_mode == 'DOOR_CREATOR':
                                # ... (код дверей без изменений) ...
                                pass

                    elif btn == sdl2.SDL_BUTTON_RIGHT:
                        keys = self.input.get_keys()
                        if self.tool_mode == 'CUBE' and self.creative_mode:
                            # ПКМ = УСТАНОВКА
                            ray_o, ray_d = self.get_world_ray()
                            # Распаковываем 4 значения, target_ent нам нужен для группы
                            size, center, _, target_ent = self._get_cube_tool_data(ray_o, ray_d, is_cutting=False)
                            
                            if center is not None:
                                new_ent = Entity(center, size)
                                # Настройки цвета/материала
                                c = self.last_paint_settings['color']
                                new_ent.faces_colors = [list(c)] * 6
                                t_path = self.last_paint_settings.get('texture_path')
                                if t_path:
                                    self.texture_manager.load_from_file(t_path)
                                    new_ent.faces_textures = [t_path] * 6
                                new_ent.faces_tiling = [self.last_paint_settings.get('is_tiling', False)] * 6
                                new_ent.density = self.last_paint_settings.get('density', 1.0)
                                refl = self.last_paint_settings.get('reflectivity', 0.0)
                                new_ent.faces_reflectivity = [refl] * 6
                                
                                # --- НОВОЕ: Наследование группы ---
                                if target_ent and target_ent.group_id:
                                    new_ent.group_id = target_ent.group_id
                                # ----------------------------------
                                
                                self.scene.add_entity(new_ent)
                                self.mark_scene_changed(changed_entities=[new_ent])
                            return
                        is_alt = keys.get(sdl2.SDLK_LALT) or keys.get(sdl2.SDLK_RALT)
                        if self.creative_mode and is_alt:
                            ray_o, ray_d = self.get_world_ray()
                            cands = self.get_candidates_for_ray(ray_o, ray_d)
                            d_ent, _, _ = self.scene.raycast(ray_o, ray_d, candidates=cands)
                            if d_ent and d_ent.is_door:
                                self.trigger_door_animation(d_ent)
                                return
                        if self.tool_mode == 'STRIP' and len(self.strip_points) > 0:
                            self.strip_points.pop()
                            if not self.strip_points:
                                self.strip_normal = None
                                self.strip_plane_p = None
                        else:
                            if self.creative_mode:
                                self.set_mouse_lock(False)
                else:
                    if self.creative_mode and btn in [sdl2.SDL_BUTTON_LEFT, sdl2.SDL_BUTTON_RIGHT]:
                        self.rect_selecting = True
                        self.rect_start = self.input.mouse_pos
                        self.rect_current = self.input.mouse_pos
        elif event.type == sdl2.SDL_MOUSEBUTTONUP:
            if self.state == "PAUSE":
                self.slider_fog.handle_event(event)
                self.slider_thick.handle_event(event)
            if self.state == "GAME" and self.creative_mode and self.color_picker.active:
                self.color_picker.handle_event(event, None) 
            if self.state == "GAME" and self.creative_mode and self.rect_selecting:
                self.rect_selecting = False
                dist = math.hypot(self.rect_current[0] - self.rect_start[0], self.rect_current[1] - self.rect_start[1])
                keys = self.input.get_keys()
                is_ctrl = keys.get(sdl2.SDLK_LCTRL, False) or keys.get(sdl2.SDLK_RCTRL, False)
                if dist > 5:
                    if self.tool_mode != 'SELECT':
                        self.build_start = None; self.cut_start_point = None; self.cut_target_ent = None
                        self.room_extruding = False; self.box_extruding = False
                        self.strip_points = []; self.strip_extruding = False
                        self.tool_mode = 'SELECT'; self.manipulation_mode = 'MOVE'; self.edit_mode = True
                    self.perform_rect_selection(self.rect_start, self.rect_current, is_ctrl)
                else:
                    if not self.color_picker.active and event.button.button == sdl2.SDL_BUTTON_LEFT:
                        self.handle_left_click()
                if not self.color_picker.active:
                    self.set_mouse_lock(True)
        elif event.type == sdl2.SDL_MOUSEWHEEL:
            # ИСПРАВЛЕНИЕ: Разрешаем менять скорость и в GAME, и в CINECAM
            if self.state == "GAME" or self.state == "CINECAM":
                dy = event.wheel.y
                
                # В режиме CINECAM мы всегда летаем, даже если зашли из выживания
                is_flying = self.creative_mode or (self.state == "CINECAM")
                
                if is_flying:
                    self.camera.speed = max(0.1, self.camera.speed + dy * 0.5)
                else:
                    # Логика фонарика только для режима выживания в игре
                    step = 2.0 
                    self.lantern_radius += dy * step
                    self.lantern_radius = max(0.0, min(150.0, self.lantern_radius))
        elif event.type == sdl2.SDL_KEYDOWN:
            key = event.key.keysym.sym
            mod_state = event.key.keysym.mod
            is_ctrl = (mod_state & sdl2.KMOD_CTRL) != 0
            is_alt = (mod_state & sdl2.KMOD_ALT) != 0
            is_shift = (mod_state & sdl2.KMOD_SHIFT) != 0
            if self.creative_mode and self.color_picker.active:
                if key == sdl2.SDLK_x:
                    pass 
                else:
                    if key == sdl2.SDLK_r: 
                        direction = -1 if is_ctrl else 1
                        states_before = {e.uid: e.to_dict() for e in self.selected_entities}
                        for ent in self.selected_entities:
                            new_uv_data = copy.deepcopy(ent.faces_uv_data)
                            faces = range(6) if self.color_picker.paint_all else self.selected_faces.get(ent, [])
                            for f in faces:
                                new_uv_data[f]['rot'] = (new_uv_data[f]['rot'] + direction) % 4
                            ent.faces_uv_data = new_uv_data
                            self.invalidate_entity_chunks(ent)
                        states_after = {e.uid: e.to_dict() for e in self.selected_entities}
                        self.scene.push_modification(states_before, states_after)
                        self.force_chunk_update = True
                        return
                    if key == sdl2.SDLK_f: 
                        states_before = {e.uid: e.to_dict() for e in self.selected_entities}
                        for ent in self.selected_entities:
                            new_uv_data = copy.deepcopy(ent.faces_uv_data)
                            faces = range(6) if self.color_picker.paint_all else self.selected_faces.get(ent, [])
                            for f in faces:
                                if is_ctrl: new_uv_data[f]['flipv'] = 1 - new_uv_data[f]['flipv']
                                else:       new_uv_data[f]['fliph'] = 1 - new_uv_data[f]['fliph']
                            ent.faces_uv_data = new_uv_data
                            self.invalidate_entity_chunks(ent)
                        states_after = {e.uid: e.to_dict() for e in self.selected_entities}
                        self.scene.push_modification(states_before, states_after)
                        self.force_chunk_update = True
                        return
                    if key == sdl2.SDLK_DELETE:
                        if self.selected_entities:
                            if self.local_tex_history_idx < len(self.local_tex_history) - 1:
                                self.local_tex_history = self.local_tex_history[:self.local_tex_history_idx+1]
                            for ent in self.selected_entities:
                                faces_to_edit = range(6)
                                if not self.color_picker.paint_all and ent in self.selected_faces:
                                    faces_to_edit = self.selected_faces[ent]
                                new_textures = list(ent.faces_textures)
                                new_uv_data = copy.deepcopy(ent.faces_uv_data)
                                for f_idx in faces_to_edit:
                                    new_textures[f_idx] = None
                                    new_uv_data[f_idx] = {'off': [0.0, 0.0], 'scl': [1.0, 1.0], 'rot': 0, 'fliph': 0, 'flipv': 0}
                                ent.faces_textures = new_textures
                                ent.faces_uv_data = new_uv_data
                                self.invalidate_entity_chunks(ent)
                            new_state = self._get_current_local_state()
                            self.local_tex_history.append(new_state)
                            self.local_tex_history_idx += 1
                            self.color_picker.set_texture_name(None)
                            self.force_chunk_update = True
                        return
                    if key == sdl2.SDLK_RETURN: self.close_color_picker(apply=True); return
                    if key == sdl2.SDLK_ESCAPE: self.close_color_picker(apply=False); return
                    if key == sdl2.SDLK_BACKSPACE:
                        self.color_picker.data_string = self.color_picker.data_string[:-1]
                        self.color_picker._update_string_texture()
                    elif key < 128:
                        char = chr(key)
                        if char.isdigit() or char in ', ':
                            self.color_picker.data_string += char
                            self.color_picker._update_string_texture()
                        try:
                            parts = [int(x.strip()) for x in self.color_picker.data_string.split(',') if x.strip().isdigit()]
                            if len(parts) >= 3:
                                r = max(0, min(255, parts[0])) / 255.0
                                g = max(0, min(255, parts[1])) / 255.0
                                b = max(0, min(255, parts[2])) / 255.0
                                a = 1.0; e = 0.0; gloss = 0.0
                                if len(parts) >= 4: a = max(0, min(100, parts[3])) / 100.0
                                if len(parts) >= 5: e = max(0, min(100, parts[4])) / 100.0
                                if len(parts) >= 6: gloss = max(0, min(100, parts[5])) / 100.0
                                if len(parts) >= 7: density = max(0, min(100, parts[6])) / 100.0
                                else: density = 1.0
                                self.color_picker.set_full_data(r, g, b, a, e, gloss, None, False, density)
                        except: pass
                    return 
            if key == sdl2.SDLK_F11:
                self.fullscreen = not self.fullscreen
                flags = sdl2.SDL_WINDOW_FULLSCREEN_DESKTOP if self.fullscreen else 0
                sdl2.SDL_SetWindowFullscreen(self.window, flags)
                self.update_window_mode(self.win_w, self.win_h) 
            if key == sdl2.SDLK_TAB:
                if self.state != "SUN_SETTINGS": 
                    self.toggle_game_mode()
                return
            if key == sdl2.SDLK_e and is_ctrl:
                if self.state == "GAME" and self.creative_mode:
                    self.sun_angle_time_backup = self.sun_angle_time
                    self.sun_angle_tilt_backup = self.sun_angle_tilt
                    self.sun_rotation_y_backup = self.sun_rotation_y
                    self.sun_speed_backup = self.sun_speed
                    self.set_state("SUN_SETTINGS")
                elif self.state == "SUN_SETTINGS":
                    self.set_state("GAME")
                return
            if key == sdl2.SDLK_RETURN:
                if self.state == "SUN_SETTINGS":
                    self.set_state("GAME")
                    return
                if self.state == "GAME" and self.creative_mode:
                    if self.tool_mode == 'DOOR_CREATOR':
                        if self.highlighted_ent:
                            edge = self.locked_hinge_edge if self.door_tool_state == 'LOCKED' else self.temp_hinge_edge
                            if edge != -1:
                                master = self.highlighted_ent
                                if master.group_id:
                                    targets = [e for e in self.scene.entities if e.group_id == master.group_id]
                                else:
                                    targets = [master]
                                states_before = {e.uid: e.to_dict() for e in targets}
                                for t in targets:
                                    t.is_door = True
                                    t.door_angle = 0.0
                                    t.door_open = False
                                    if t == master: t.hinge_edge = edge
                                    else: t.hinge_edge = -1 
                                states_after = {e.uid: e.to_dict() for e in targets}
                                self.scene.push_modification(states_before, states_after)
                                self.mark_scene_changed(changed_entities=targets)
                                self.door_tool_state = 'HOVER'
                                self.locked_hinge_edge = -1
                                self.show_notification(self.tr('NOTIF_DOOR_CREATED'))
                        return
            if key == sdl2.SDLK_ESCAPE:
                if self.state == "SUN_SETTINGS":
                    self.sun_angle_time = self.sun_angle_time_backup
                    self.sun_angle_tilt = self.sun_angle_tilt_backup
                    self.sun_rotation_y = self.sun_rotation_y_backup
                    self.sun_speed = self.sun_speed_backup 
                    self.set_state("GAME")
                    return
                if self.state == "CONFIRM_SAVE":
                    self.pending_exit_action = None
                    self.set_state("GAME")
                    return
                if self.state == "PAUSE":
                    self.set_state("GAME")
                    return
                if self.state == "GAME":
                    if not self.mouse_locked or self.rect_selecting:
                        self.exit_rect_selection(); return
                    if self.tool_mode == 'DOOR_CREATOR':
                        if self.door_tool_state == 'LOCKED':
                            self.door_tool_state = 'HOVER'
                            self.locked_hinge_edge = -1
                        else:
                            self.tool_mode = 'SELECT'
                            self.door_tool_state = 'HOVER'
                            self.highlighted_ent = None
                        return
                    if self.build_start is not None or self.cut_start_point is not None or \
                       self.cut_target_ent is not None or self.room_extruding or self.box_extruding:
                        self.build_start = None; self.cut_start_point = None; self.cut_target_ent = None
                        self.room_extruding = False; self.box_extruding = False; self.visual_cursor_pos = None
                        return
                    if self.tool_mode == 'STRIP' and (self.strip_points or self.strip_extruding):
                        self.strip_points = []; self.strip_extruding = False; self.build_start = None
                        return 
                    if self.tool_mode != 'SELECT' or self.manipulation_mode == 'RESIZE':
                        self.tool_mode = 'SELECT'; self.manipulation_mode = 'MOVE'; self.edit_mode = True
                        return
                    if self.selected_entities:
                        self.selected_entities = []; self.selected_faces = {}
                        return
                    self.set_state("PAUSE")
                return
            if self.state == "GAME" and self.creative_mode:
                if key == sdl2.SDLK_t:
                    if is_ctrl:
                        affected_entities = []
                        if self.tool_mode == 'SELECT' and self.selected_entities:
                            processed_groups = set()
                            for ent in self.selected_entities:
                                if not ent.is_door: continue
                                if ent.group_id:
                                    if ent.group_id in processed_groups: continue
                                    processed_groups.add(ent.group_id)
                                    group_members = [e for e in self.scene.entities if e.group_id == ent.group_id]
                                    affected_entities.extend(group_members)
                                else:
                                    affected_entities.append(ent)
                        elif self.tool_mode == 'DOOR_CREATOR':
                            ray_o, ray_d = self.get_world_ray()
                            d_ent, _, _ = self.scene.raycast(ray_o, ray_d)
                            if d_ent and d_ent.is_door:
                                if d_ent.group_id: affected_entities = [e for e in self.scene.entities if e.group_id == d_ent.group_id]
                                else: affected_entities = [d_ent]
                        if affected_entities:
                            states_before = {e.uid: e.to_dict() for e in affected_entities}
                            for t in affected_entities: t.door_open = not t.door_open
                            states_after = {e.uid: e.to_dict() for e in affected_entities}
                            self.scene.push_modification(states_before, states_after)
                            self.mark_scene_changed(changed_entities=affected_entities)
                            self.show_notification(self.tr('NOTIF_DOOR_FLIPPED'))
                        return
                    self.exit_rect_selection()
                    if self.tool_mode == 'DOOR_CREATOR':
                        self.tool_mode = 'SELECT'
                        self.door_tool_state = 'HOVER'
                        self.highlighted_ent = None
                    else:
                        self.tool_mode = 'DOOR_CREATOR'
                        self.door_tool_state = 'HOVER'
                        self.build_start = None
                        self.selected_entities = []
                    return
                if key == sdl2.SDLK_1:
                    self.exit_rect_selection(); self.visual_cursor_pos = None 
                    if self.tool_mode == 'WALL': self.tool_mode = 'SELECT'; self.manipulation_mode = 'MOVE'; self.edit_mode = True
                    else: self.tool_mode = 'WALL'; self.edit_mode = False; self.build_start = None; self.constraint_axis = 1; self.selected_entities = []
                if key == sdl2.SDLK_2:
                    self.exit_rect_selection(); self.visual_cursor_pos = None 
                    if self.tool_mode == 'BOX': self.tool_mode = 'SELECT'; self.manipulation_mode = 'MOVE'; self.edit_mode = True
                    else: self.tool_mode = 'BOX'; self.edit_mode = False; self.build_start = None; self.box_extruding = False; self.selected_entities = []
                if key == sdl2.SDLK_3:
                    self.exit_rect_selection(); self.visual_cursor_pos = None 
                    if self.tool_mode == 'ROOM': self.tool_mode = 'SELECT'; self.manipulation_mode = 'MOVE'; self.edit_mode = True
                    else: self.tool_mode = 'ROOM'; self.edit_mode = False; self.build_start = None; self.room_extruding = False; self.constraint_axis = 1; self.selected_entities = []
                if key == sdl2.SDLK_4:
                    self.exit_rect_selection(); self.visual_cursor_pos = None 
                    if self.tool_mode == 'STRIP': self.tool_mode = 'SELECT'; self.manipulation_mode = 'MOVE'; self.edit_mode = True
                    else: self.tool_mode = 'STRIP'; self.edit_mode = False; self.strip_points = []; self.strip_extruding = False; self.selected_entities = []
                if key == sdl2.SDLK_5:
                    self.exit_rect_selection(); self.visual_cursor_pos = None
                    if self.tool_mode == 'CUBE': 
                        self.tool_mode = 'SELECT'; self.manipulation_mode = 'MOVE'; self.edit_mode = True
                    else: 
                        self.tool_mode = 'CUBE'; self.edit_mode = False
                        

                # --- СДВИГ ОСТАЛЬНЫХ (6, 7) ---
                if key == sdl2.SDLK_6:
                    self.visual_cursor_pos = None 
                    if self.tool_mode == 'CUT': self.tool_mode = 'SELECT'; self.manipulation_mode = 'MOVE'; self.edit_mode = True
                    else: self.tool_mode = 'CUT'; self.edit_mode = False; self.cut_start_point = None
                
                if key == sdl2.SDLK_7:
                    self.exit_rect_selection(); self.visual_cursor_pos = None 
                    if self.tool_mode == 'SLICE': self.tool_mode = 'SELECT'; self.manipulation_mode = 'MOVE'; self.edit_mode = True
                    else: self.tool_mode = 'SLICE'; self.edit_mode = False; self.slice_orientation = 0
                if key == sdl2.SDLK_e:
                    self.exit_rect_selection()
                    if self.tool_mode == 'SELECT' and self.manipulation_mode == 'RESIZE': self.manipulation_mode = 'MOVE'
                    else: self.tool_mode = 'SELECT'; self.edit_mode = True; self.manipulation_mode = 'RESIZE'; self.build_start = None
                if key == sdl2.SDLK_x:
                    if is_ctrl: 
                        target_ent = None; face_idx = 2
                        if self.selected_entities:
                            target_ent = self.selected_entities[-1]
                            if target_ent in self.selected_faces and self.selected_faces[target_ent]:
                                face_idx = list(self.selected_faces[target_ent])[-1]
                        else:
                            ray_o, ray_d = self.get_world_ray()
                            ent, _, norm = self.scene.raycast(ray_o, ray_d, ignore_holes=True)
                            if ent:
                                target_ent = ent
                                f_idx = self.get_face_index_from_norm(norm)
                                if f_idx is not None: face_idx = f_idx
                        if target_ent:
                            c = target_ent.faces_colors[face_idx]
                            r, g, b = c[0], c[1], c[2]
                            a = c[3] if len(c) > 3 else 1.0
                            e = c[4] if len(c) > 4 else 0.0
                            gloss = c[5] if len(c) > 5 else 0.0
                            is_tiling = target_ent.faces_tiling[face_idx]
                            dens = target_ent.density
                            refl = getattr(target_ent, 'reflectivity', 0.0) 
                            tex_path = target_ent.faces_textures[face_idx]
                            self.color_picker.set_full_data(r, g, b, a, e, gloss, tex_path, is_tiling, dens, refl)
                            self.last_paint_settings = {
                                'color': [r, g, b, a, e, gloss], 
                                'all': self.color_picker.paint_all,
                                'is_tiling': is_tiling,
                                'density': dens,
                                'reflectivity': refl, 
                                'texture_path': tex_path
                            }
                            self.show_notification(self.tr('NOTIF_PROPS_COPIED'))
                    else: 
                        now = pygame.time.get_ticks()
                        if now - self.last_x_press < 300: 
                            ls = self.last_paint_settings
                            col = ls['color']
                            is_tiling = ls.get('is_tiling', False)
                            density_val = ls.get('density', 1.0)
                            refl_val = ls.get('reflectivity', 0.0) 
                            t_path = ls.get('texture_path', None)
                            paint_all = True
                            if self.selected_entities:
                                target_ent = self.selected_entities[-1]
                                if target_ent in self.selected_faces and self.selected_faces[target_ent]:
                                    paint_all = False
                            self.apply_paint(col, paint_all, is_tiling, density_val, t_path, refl_val)
                            if self.color_picker.active: 
                                self.tex_session_active = False 
                                self.close_color_picker(apply=False)
                            self.show_notification(self.tr('NOTIF_SETTINGS_APPLIED'))
                        else:
                            if not self.color_picker.active: self.open_color_picker()
                            else: self.close_color_picker(apply=False)
                        self.last_x_press = now
                if key == sdl2.SDLK_s and is_ctrl and is_alt:
                    self.quick_save()
                if event.key.keysym.scancode == sdl2.SDL_SCANCODE_G:
                    if not is_ctrl and not is_alt:
                        if self.tool_mode == 'SELECT' and self.selected_entities:
                            states_before = {e.uid: e.to_dict() for e in self.selected_entities}
                            
                            unique_gids = {e.group_id for e in self.selected_entities}
                            is_single_group = (len(unique_gids) == 1 and list(unique_gids)[0] is not None)
                            
                            should_ungroup = False
                            if is_single_group:
                                gid = list(unique_gids)[0]
                                all_members = [e for e in self.scene.entities if e.group_id == gid]
                                # Если выбраны ВСЕ члены группы - разгруппировываем
                                if len(self.selected_entities) == len(all_members): 
                                    should_ungroup = True
                            
                            if should_ungroup:
                                # РАЗГРУППИРОВКА
                                for ent in self.selected_entities:
                                    if ent.group_history: 
                                        ent.group_id = ent.group_history.pop()
                                    else: 
                                        ent.group_id = None
                                self.show_notification(self.tr('NOTIF_GROUP_DISSOLVED')) # <-- Уведомление
                            else: 
                                # СОЗДАНИЕ ГРУППЫ
                                new_gid = uuid.uuid4().hex
                                for ent in self.selected_entities:
                                    if ent.group_id is not None: 
                                        ent.group_history.append(ent.group_id)
                                    ent.group_id = new_gid
                                self.show_notification(self.tr('NOTIF_GROUP_CREATED')) # <-- Уведомление
                            
                            states_after = {e.uid: e.to_dict() for e in self.selected_entities}
                            self.scene.push_modification(states_before, states_after)
                            self.unsaved_changes = True
                if key == sdl2.SDLK_c:
                    if is_ctrl: 
                        # Ctrl+C = Копирование
                        if self.tool_mode == 'SELECT' and self.selected_entities:
                            self.clipboard = [e.to_dict() for e in self.selected_entities]
                            self.show_notification(self.tr('NOTIF_COPIED'))
                    else:
                        # C (без Ctrl) = Переключение режима камеры
                        if self.creative_mode and self.state == "GAME":
                            self.tool_mode = 'SELECT'
                            self.manipulation_mode = 'MOVE'
                            self.build_start = None
                            self.cut_start_point = None
                            self.strip_points = []
                            self.strip_extruding = False
                            self.room_extruding = False
                            self.box_extruding = False
                            self.door_tool_state = 'HOVER'
                            self.highlighted_ent = None
                            self.set_state("CINECAM")
                            self.show_notification(self.tr('NOTIF_CINE_ON'))
                if key == sdl2.SDLK_v and is_ctrl: 
                    if self.clipboard:
                        ray_o, ray_d = self.get_world_ray()
                        hit_ent, hit_dist, hit_norm = self.scene.raycast(ray_o, ray_d)
                        grp_min = np.array([np.inf]*3); grp_max = np.array([-np.inf]*3)
                        for d in self.clipboard:
                            pos = np.array(d['position']); scale = np.array(d['scale'])
                            grp_min = np.minimum(grp_min, pos - scale/2); grp_max = np.maximum(grp_max, pos + scale/2)
                        grp_center = (grp_min + grp_max) / 2.0
                        grp_size = grp_max - grp_min
                        offset_surf = np.zeros(3)
                        if hit_ent:
                            target_pos = ray_o + ray_d * hit_dist
                            if hit_norm is not None:
                                axis = np.argmax(np.abs(hit_norm)); sign = np.sign(hit_norm[axis])
                                offset_surf[axis] = (grp_size[axis] / 2.0) * sign
                                target_pos += hit_norm * 0.001
                        else:
                            gr_p = self.get_ground_intersect(ray_o, ray_d)
                            if gr_p is not None: target_pos = gr_p; offset_surf[1] = grp_size[1] / 2.0
                            else: target_pos = ray_o + ray_d * 5.0
                        final_pos = target_pos + offset_surf
                        move_delta = snap_vector(final_pos - grp_center, self.snap_unit)
                        self.selected_entities = []; new_selection = []; grp_map = {}
                        added_entities = [] 
                        for data in self.clipboard:
                            new_ent = Entity.from_dict(data)
                            new_ent.uid = uuid.uuid4().hex
                            new_ent.pos = np.array(new_ent.pos) + move_delta
                            new_ent.pos, new_ent.scale = snap_bounds_to_grid_3d(new_ent.pos, new_ent.scale, precision=0.01)
                            if new_ent.group_id:
                                if new_ent.group_id not in grp_map: grp_map[new_ent.group_id] = uuid.uuid4().hex
                                new_ent.group_id = grp_map[new_ent.group_id]
                            self.scene.entities.append(new_ent)
                            new_selection.append(new_ent)
                            added_entities.append(new_ent)
                        self.selected_entities = new_selection
                        self.tool_mode = 'SELECT'; self.manipulation_mode = 'MOVE'; self.edit_mode = True
                        if added_entities:
                            self.scene.push_transaction(
                                added_ents=added_entities, 
                                removed_ents=[], 
                                modified_triplets=[]
                            )
                            self.mark_scene_changed(changed_entities=added_entities)
                if key == sdl2.SDLK_r and self.tool_mode == 'SELECT': self.rotate_selection()
                if key == sdl2.SDLK_f and self.tool_mode == 'SELECT': self.mirror_selection()
                if key == sdl2.SDLK_q:
                    if self.tool_mode == 'SELECT':
                        if is_ctrl or is_shift: self.transform_axis = (self.transform_axis + 1) % 3
                        else: self.transform_axis = 1 if self.transform_axis != 1 else 0
                        self.vertical_mode = (self.transform_axis == 1)
                    elif self.build_start is not None: self.constraint_axis = (self.constraint_axis + 1) % 3
                    elif self.tool_mode == 'SLICE': self.slice_orientation = 1 - self.slice_orientation
                if key == sdl2.SDLK_DELETE and self.selected_entities:
                    self.exit_rect_selection()
                    deleted_list = list(self.selected_entities)
                    for ent in deleted_list:
                        if ent in self.scene.entities:
                            self.scene.entities.remove(ent)
                    self.scene.push_transaction(
                        added_ents=[], 
                        removed_ents=deleted_list, 
                        modified_triplets=[]
                    )
                    self.selected_entities = []
                    self.mark_scene_changed(changed_entities=deleted_list)
                    self.show_notification(self.tr('NOTIF_OBJ_DELETED'))
                if self.tool_mode == 'SELECT' and self.selected_entities:
                    if not self.color_picker.active:
                        if key in [sdl2.SDLK_UP, sdl2.SDLK_DOWN, sdl2.SDLK_LEFT, sdl2.SDLK_RIGHT]:
                            self.apply_keyboard_manipulation(key, self.input.get_keys())
                            self.last_manipulation_time = pygame.time.get_ticks() + 400
    def _get_cube_tool_data(self, ray_o, ray_d, is_cutting):
        keys = self.input.get_keys()
        is_alt = keys.get(sdl2.SDLK_LALT) or keys.get(sdl2.SDLK_RALT) 
        is_ctrl = keys.get(sdl2.SDLK_LCTRL) or keys.get(sdl2.SDLK_RCTRL)

        # 1. Определение размера и шага сетки
        if is_alt:
            # Большой блок (0.5м)
            size_val = 0.5
            snap_step = 0.25
        elif is_ctrl:
            # Мелкая детализация (1см)
            size_val = 0.01
            snap_step = 0.01
        else:
            # Стандартный куб (1дм)
            size_val = 0.1
            snap_step = 0.1 

        size_vec = np.array([size_val, size_val, size_val], dtype=np.float32)

        # 2. Поиск точки пересечения
        cands = self.get_candidates_for_ray(ray_o, ray_d)
        ent, dist, norm = self.scene.raycast(ray_o, ray_d, ignore_holes=True, candidates=cands)
        
        hit_pos = None
        if ent and norm is not None:
            hit_pos = ray_o + ray_d * dist
        else:
            hit_pos = self.get_ground_intersect(ray_o, ray_d)
            if hit_pos is not None:
                norm = np.array([0.0, 1.0, 0.0])

        if hit_pos is None:
            return None, None, None, None # Возвращаем 4 значения

        # Определяем ось, перпендикулярную поверхности
        axis = np.argmax(np.abs(norm))
        final_center = np.zeros(3, dtype=np.float32)

        for i in range(3):
            if i == axis:
                # Вдоль нормали: ИДЕАЛЬНОЕ ПРИЛЕГАНИЕ (без snap)
                coord = hit_pos[i]
                if not is_cutting:
                    # ПКМ (Ставим): сдвигаем наружу на пол-размера
                    coord += norm[i] * (size_val / 2.0)
                else:
                    # ЛКМ (Режем)
                    if is_ctrl:
                        # Ctrl: сдвигаем внутрь на пол-размера (чтобы грань была вровень)
                        coord -= norm[i] * (size_val / 2.0)
                    else:
                        # Alt/Std: Центр ровно на поверхности (режет на 50% глубины)
                        pass 
                final_center[i] = coord
            else:
                # Вдоль плоскости: ПРИВЯЗКА К СЕТКЕ
                final_center[i] = snap_value(hit_pos[i], snap_step)

        # Возвращаем размер, центр, нормаль И ОБЪЕКТ
        return size_vec, final_center, norm, ent
    def perform_cube_cut(self, center, size):
        half = size / 2.0
        c_min = center - half
        c_max = center + half
        
        targets = []
        # Если есть выделение - режем ТОЛЬКО выделенное (включая группы)
        if self.selected_entities:
            targets = list(self.selected_entities)
        else:
            # Иначе ищем пересечения по всему миру
            for ent in self.scene.entities:
                if ent.is_hole: continue
                e_min, e_max = ent.get_aabb()
                if (c_min[0] < e_max[0] and c_max[0] > e_min[0] and
                    c_min[1] < e_max[1] and c_max[1] > e_min[1] and
                    c_min[2] < e_max[2] and c_max[2] > e_min[2]):
                    targets.append(ent)

        if not targets: return

        added = []
        removed = []
        
        # Увеличенный epsilon для защиты от микро-артефактов при многократном резе
        eps = 1e-4 
        
        for ent in targets:
            e_min, e_max = ent.get_aabb()
            
            # Пересечение объекта и резака
            i_min = np.maximum(e_min, c_min)
            i_max = np.minimum(e_max, c_max)
            
            # Если реального пересечения нет
            if np.any(i_min >= i_max - eps): continue
            
            removed.append(ent)
            
            # Функция-хелпер для безопасного создания куска
            def safe_add(p_min, p_max):
                # Проверяем размеры по всем осям
                dims = p_max - p_min
                if np.all(dims > eps):
                    added.append(self._create_fragment_ent(ent, p_min, p_max))

            # 1. TOP (Y+)
            if e_max[1] > i_max[1]:
                safe_add(np.array([e_min[0], i_max[1], e_min[2]]), 
                         np.array([e_max[0], e_max[1], e_max[2]]))
                
            # 2. BOTTOM (Y-)
            if e_min[1] < i_min[1]:
                safe_add(np.array([e_min[0], e_min[1], e_min[2]]), 
                         np.array([e_max[0], i_min[1], e_max[2]]))
                
            y0, y1 = i_min[1], i_max[1]
            
            # 3. LEFT (X-)
            if e_min[0] < i_min[0]:
                safe_add(np.array([e_min[0], y0, e_min[2]]), 
                         np.array([i_min[0], y1, e_max[2]]))
                
            # 4. RIGHT (X+)
            if e_max[0] > i_max[0]:
                safe_add(np.array([i_max[0], y0, e_min[2]]), 
                         np.array([e_max[0], y1, e_max[2]]))
            
            x0, x1 = i_min[0], i_max[0]
            
            # 5. BACK (Z-)
            if e_min[2] < i_min[2]:
                safe_add(np.array([x0, y0, e_min[2]]), 
                         np.array([x1, y1, i_min[2]]))
                
            # 6. FRONT (Z+)
            if e_max[2] > i_max[2]:
                safe_add(np.array([x0, y0, i_max[2]]), 
                         np.array([x1, y1, e_max[2]]))

        # Удаляем старые
        for e in removed:
            if e in self.scene.entities: self.scene.entities.remove(e)
            
        # Добавляем новые
        for e in added:
            self.scene.entities.append(e)
            
        # ОБНОВЛЕНИЕ ВЫДЕЛЕНИЯ:
        # Если мы резали уже выделенные объекты, то выделение должно "перетечь" на новые куски.
        # Если ничего не было выделено (резали без выделения), то added не выделяем (стандартное поведение).
        if self.selected_entities and removed:
            # Убираем удаленные из списка выделения
            for rem in removed:
                if rem in self.selected_entities:
                    self.selected_entities.remove(rem)
            
            # Добавляем новые куски в выделение
            self.selected_entities.extend(added)

        if added or removed:
            self.scene.push_transaction(added, removed, [])
            self.mark_scene_changed(changed_entities=added)
            self.show_notification(self.tr('NOTIF_CUBE_CUT'))

    def _create_fragment_ent(self, parent, min_p, max_p):
        center = (min_p + max_p) / 2.0
        size = max_p - min_p
        
        # Защита от нулевых размеров (если float error)
        size = np.maximum(size, 0.001)
        
        new_ent = Entity(center, size, parent.group_id)
        # Копируем свойства
        new_ent.faces_colors = copy.deepcopy(parent.faces_colors)
        new_ent.faces_textures = list(parent.faces_textures)
        new_ent.faces_tiling = list(parent.faces_tiling)
        new_ent.faces_uv_data = copy.deepcopy(parent.faces_uv_data)
        new_ent.faces_reflectivity = list(parent.faces_reflectivity)
        new_ent.density = parent.density
        new_ent.group_history = list(parent.group_history)
        
        # Сохраняем позицию текстуры
        TextureUtils.preserve_texture_pos(parent, new_ent)
        
        return new_ent
    def _get_current_local_state(self):
        state = {}
        for ent in self.selected_entities:
            state[ent.uid] = {
                'uv': copy.deepcopy(ent.faces_uv_data),
                'tex': list(ent.faces_textures),
                'tiling': list(ent.faces_tiling),
                'reflectivity': list(ent.faces_reflectivity), 
                'density': ent.density,
                'colors': copy.deepcopy(ent.faces_colors) 
            }
        return state
    def _apply_live_ui_changes(self):
        if not self.selected_entities: return
        full_data = self.color_picker.get_full_data()
        r, g, b = full_data[0], full_data[1], full_data[2]
        a = full_data[3]
        emit = full_data[4]
        gloss = full_data[5]
        new_color_list = [r, g, b, a, emit, gloss]
        is_tiling_ui = full_data[7]
        density_ui = full_data[8]
        reflectivity_ui = full_data[9]
        changed = False
        for ent in self.selected_entities:
            if abs(ent.density - density_ui) > 0.001:
                ent.density = density_ui
                changed = True
            target_faces = range(6)
            if not self.color_picker.paint_all and ent in self.selected_faces and self.selected_faces[ent]:
                target_faces = self.selected_faces[ent]
            for f_idx in target_faces:
                if ent.faces_tiling[f_idx] != is_tiling_ui:
                    ent.faces_tiling[f_idx] = is_tiling_ui
                    changed = True
                if not hasattr(ent, 'faces_reflectivity'):
                    ent.faces_reflectivity = [0.0] * 6
                if abs(ent.faces_reflectivity[f_idx] - reflectivity_ui) > 0.001:
                    ent.faces_reflectivity[f_idx] = reflectivity_ui
                    changed = True
                current_col = ent.faces_colors[f_idx]
                if current_col[:6] != new_color_list:
                    ent.faces_colors[f_idx] = list(new_color_list)
                    changed = True
            if changed:
                self.invalidate_entity_chunks(ent)    
        if changed:
            new_state = self._get_current_local_state()
            if self.local_tex_history_idx < len(self.local_tex_history) - 1:
                self.local_tex_history = self.local_tex_history[:self.local_tex_history_idx+1]
            self.local_tex_history.append(new_state)
            self.local_tex_history_idx += 1
            self.force_chunk_update = True
    def process_continuous(self, dt):
        if hasattr(self, 'file_dialog') and self.file_dialog.active:
            self.file_dialog.update() 
            return
        keys = self.input.get_keys()
        is_ctrl = keys.get(sdl2.SDLK_LCTRL) or keys.get(sdl2.SDLK_RCTRL)
        if is_ctrl and self.state != "CINECAM":
            now = pygame.time.get_ticks()
            if now > self.undo_redo_timer:
                if keys.get(sdl2.SDLK_z):
                    if self.creative_mode and self.color_picker.active and self.tex_session_active:
                        if self.local_tex_history_idx > 0:
                            self.local_tex_history_idx -= 1
                            state = self.local_tex_history[self.local_tex_history_idx]
                            for uid, data in state.items():
                                ent = self.scene.get_entity_by_uid(uid)
                                if ent:
                                    ent.faces_uv_data = copy.deepcopy(data['uv'])
                                    ent.faces_textures = list(data['tex'])
                                    if 'tiling' in data:
                                        ent.faces_tiling = list(data['tiling'])
                                    else:
                                        val = data.get('tiling_bool', False)
                                        ent.faces_tiling = [val] * 6
                                    ent.density = data.get('density', 1.0)
                                    if 'reflectivity' in data:
                                        ent.faces_reflectivity = list(data['reflectivity'])
                                    if 'colors' in data:
                                        ent.faces_colors = copy.deepcopy(data['colors'])
                                    self.invalidate_entity_chunks(ent)
                            self.force_chunk_update = True
                            self._sync_color_picker_ui()
                    else:
                        self.perform_undo()
                    self.undo_redo_timer = now + self.repeat_interval
                elif keys.get(sdl2.SDLK_y):
                    if self.creative_mode and self.color_picker.active and self.tex_session_active:
                        if self.local_tex_history_idx < len(self.local_tex_history) - 1:
                            self.local_tex_history_idx += 1
                            state = self.local_tex_history[self.local_tex_history_idx]
                            for uid, data in state.items(): 
                                ent = self.scene.get_entity_by_uid(uid)
                                if ent:
                                    ent.faces_uv_data = copy.deepcopy(data['uv'])
                                    ent.faces_textures = list(data['tex'])
                                    if 'tiling' in data:
                                        ent.faces_tiling = list(data['tiling'])
                                    else:
                                        val = data.get('tiling_bool', False)
                                        ent.faces_tiling = [val] * 6
                                    ent.density = data.get('density', 1.0)
                                    if 'reflectivity' in data:
                                        ent.faces_reflectivity = list(data['reflectivity'])
                                    if 'colors' in data:
                                        ent.faces_colors = copy.deepcopy(data['colors'])
                                    self.invalidate_entity_chunks(ent)
                            self.force_chunk_update = True
                            self._sync_color_picker_ui()
                    else:
                        self.perform_redo()
                    self.undo_redo_timer = now + self.repeat_interval
        if (self.state == "GAME" or self.state == "SUN_SETTINGS" or self.state == "CINECAM") and self.mouse_locked:
            keys = self.input.get_keys()
            dx, dy = self.input.get_mouse_rel()
            self.camera.process_mouse(dx, dy)
            if self.creative_mode: self.camera.move(keys, dt)
            else: self.update_adventure_physics(keys, dt)
        self.update_door_animations(dt)
        if self.state == "GAME" and self.creative_mode and self.tool_mode == 'SELECT' and self.selected_entities:
            if not self.color_picker.active: 
                keys = self.input.get_keys()
                active_arrow = None
                if keys.get(sdl2.SDLK_UP): active_arrow = sdl2.SDLK_UP
                elif keys.get(sdl2.SDLK_DOWN): active_arrow = sdl2.SDLK_DOWN
                elif keys.get(sdl2.SDLK_LEFT): active_arrow = sdl2.SDLK_LEFT
                elif keys.get(sdl2.SDLK_RIGHT): active_arrow = sdl2.SDLK_RIGHT
                if active_arrow:
                    now = pygame.time.get_ticks()
                    if now > self.last_manipulation_time:
                        self.apply_keyboard_manipulation(active_arrow, keys)
                        self.last_manipulation_time = now + 100
    def _sync_color_picker_ui(self):
        if not self.selected_entities: return
        tgt = self.selected_entities[-1]
        f_idx = 2
        if tgt in self.selected_faces and self.selected_faces[tgt]:
            f_idx = list(self.selected_faces[tgt])[-1]
        c = tgt.faces_colors[f_idx]
        t_path = tgt.faces_textures[f_idx]
        is_tiling_val = tgt.faces_tiling[f_idx]
        refl = tgt.faces_reflectivity[f_idx]
        self.color_picker.set_full_data(
                                    c[0], c[1], c[2], 
                                    c[3] if len(c)>3 else 1.0, 
                                    c[4] if len(c)>4 else 0.0, 
                                    c[5] if len(c)>5 else 0.0,
                                    t_path, 
                                    is_tiling_val,
                                    tgt.density,
                                    refl 
                                )
    def run(self):
        self._init_render_context()
        while self.running:
            self.input.reset_per_frame()
            self.labels_to_draw_queue = []
            self._handle_events()
            self.label_pool_idx = 0
            dt = self.clock.get_time() / 1000.0
            self._update_logic(dt)
            self._render_frame(dt)
            sdl2.SDL_GL_SwapWindow(self.window)
            if self.limit_fps:
                self.clock.tick(self.target_refresh_rate if hasattr(self, 'target_refresh_rate') else 60)
            else:
                self.clock.tick(0)
        self._cleanup()
    def _get_mirror_check_points(self, ent, cam_pos):
        min_p, max_p = ent.get_aabb()
        center = (min_p + max_p) / 2.0
        axis = np.argmin(ent.scale)
        sign = np.sign(cam_pos[axis] - center[axis])
        if sign == 0: sign = 1.0
        face_coord = center[axis] + (ent.scale[axis] / 2.0 + 0.01) * sign
        axes = [0, 1, 2]
        axes.remove(axis)
        u, v = axes
        shrink = 0.90
        u_half = (ent.scale[u] / 2.0) * shrink
        v_half = (ent.scale[v] / 2.0) * shrink
        points = []
        p_center = center.copy()
        p_center[axis] = face_coord
        points.append(p_center)
        offsets = [(-1, -1), (1, -1), (1, 1), (-1, 1)]
        for ou, ov in offsets:
            p = center.copy()
            p[axis] = face_coord
            p[u] += u_half * ou
            p[v] += v_half * ov
            points.append(p)
        return points
    def _init_render_context(self):
        self.update_window_mode(self.win_w, self.win_h)
        mode = sdl2.SDL_DisplayMode()
        if sdl2.SDL_GetCurrentDisplayMode(0, ctypes.byref(mode)) == 0:
            self.target_refresh_rate = mode.refresh_rate if mode.refresh_rate > 0 else 60
        else:
            self.target_refresh_rate = 60
    def _render_specific_entity_internal(self, ent):
        batches = ChunkMeshBuilder.build_chunk_data([ent], (0,0,0), self.texture_manager)
        # Исправлено распаковывание ключа
        for (tex_id, mode, is_trans), data_array in batches.items():
            if len(data_array) == 0: continue
            glActiveTexture(GL_TEXTURE0)
            glBindTexture(GL_TEXTURE_2D, tex_id)
            glUniform1i(glGetUniformLocation(self.shader.program, "uTexType"), mode)
            mesh = MeshBuffer(data_array)
            mesh.draw()
            mesh.delete()
    def _cleanup(self):
        sdl2.SDL_GL_DeleteContext(self.gl_context)
        sdl2.SDL_DestroyWindow(self.window)
        sdl2.SDL_Quit()
        sys.exit()
    def _handle_events(self):
        event = sdl2.SDL_Event()
        while sdl2.SDL_PollEvent(ctypes.byref(event)) != 0:
            if event.type == sdl2.SDL_QUIT:
                self.running = False
            elif event.type == sdl2.SDL_WINDOWEVENT:
                if event.window.event == sdl2.SDL_WINDOWEVENT_RESIZED:
                    self._handle_resize()
            self.input.process_event(event)
            self.process_sdl_event(event)
    def _handle_resize(self):
        dw, dh = ctypes.c_int(), ctypes.c_int()
        ww, wh = ctypes.c_int(), ctypes.c_int()
        sdl2.SDL_GL_GetDrawableSize(self.window, dw, dh)
        sdl2.SDL_GetWindowSize(self.window, ww, wh)
        self.draw_w, self.draw_h = dw.value, dh.value
        self.win_w, self.win_h = ww.value, wh.value
        self.update_window_mode(self.win_w, self.win_h)
    def _update_logic(self, dt):
        # --- ЛОГИКА ПАУЗЫ ВРЕМЕНИ ---
        game_dt = dt
        if self.state == "PAUSE" or self.state == "CONFIRM_SAVE":
            if self.state == "PAUSE":
                self.default_thickness = round(self.slider_thick.value, 3)
                self.fog_distance = self.slider_fog.value
            game_dt = 0.0 # Полная остановка времени в меню
        # ---------------------------

        if self.state == "CINECAM":
            ray_o, ray_d = self.get_world_ray()
            self.cine_cam.update(game_dt, ray_o, ray_d) # <-- Передаем game_dt
        self.cloud_renderer.update(game_dt, self.sun_speed) # Облака стоят
        self.texture_manager.update(game_dt) # Текстуры не мерцают
        self.process_texture_input(game_dt)
        self.process_continuous(game_dt) # Двери и физика замирают
        if not self.creative_mode:
            # --- ИЗМЕНЕНИЕ: Скорость 6.0 для мягкости (было 15.0) ---
            self.camera.update_smooth_y(game_dt, speed=6.0)
        else:
            self.camera.visual_y = self.camera.pos[1]
        self.sun_angle_time += self.sun_speed * game_dt # Солнце стоит
        self.sun_angle_time %= 360.0
        if self.state == "SUN_SETTINGS":
            keys = self.input.get_keys()
            is_ctrl = keys.get(sdl2.SDLK_LCTRL) or keys.get(sdl2.SDLK_RCTRL)
            manual_speed = 60.0 * dt 
            s = abs(self.sun_speed)
            acceleration = 0.1 + s/3
            dynamic_step = acceleration * dt
            if keys.get(sdl2.SDLK_UP):
                if is_ctrl:
                    was_negative = self.sun_speed < -0.001
                    self.sun_speed += dynamic_step
                    if was_negative and self.sun_speed >= 0:
                        self.sun_speed = 0.0
                else:
                    self.sun_angle_time += manual_speed
            if keys.get(sdl2.SDLK_DOWN):
                if is_ctrl:
                    was_positive = self.sun_speed > 0.001
                    self.sun_speed -= dynamic_step
                    if was_positive and self.sun_speed <= 0:
                        self.sun_speed = 0.0
                else:
                    self.sun_angle_time -= manual_speed
            self.sun_speed = max(-25.0, min(25.0, self.sun_speed))
            if keys.get(sdl2.SDLK_LEFT):  self.sun_rotation_y -= manual_speed
            if keys.get(sdl2.SDLK_RIGHT): self.sun_rotation_y += manual_speed
            self.sun_rotation_y %= 360.0
        rad_time = math.radians(self.sun_angle_time)
        rad_tilt = math.radians(self.sun_angle_tilt)
        rad_rot  = math.radians(self.sun_rotation_y)
        base_x = math.cos(rad_time)
        base_y = math.sin(rad_time)
        base_z = math.tan(rad_tilt) 
        c_rot = math.cos(rad_rot)
        s_rot = math.sin(rad_rot)
        final_x = base_x * c_rot - base_z * s_rot
        final_y = base_y
        final_z = base_x * s_rot + base_z * c_rot
        sun_vec = np.array([final_x, final_y, final_z], dtype=np.float32)
        norm = np.linalg.norm(sun_vec)
        if norm > 0: sun_vec /= norm
        else: sun_vec = np.array([0.0, 1.0, 0.0], dtype=np.float32)
        h = sun_vec[1] 
        day_factor = self.smoothstep(-0.05, 0.15, h)
        sunset_center = -0.02
        sunset_width = 0.14
        dist = abs(h - sunset_center)
        raw_factor = 1.0 - (dist / sunset_width)
        raw_factor = max(0.0, min(1.0, raw_factor))
        sunset_factor = self.smoothstep(0.0, 1.0, raw_factor)
        c_day = np.array([0.529, 0.808, 0.922], dtype=np.float32)
        c_night = np.array([0.02, 0.02, 0.05], dtype=np.float32)
        c_sunset = np.array([0.98, 0.45, 0.25], dtype=np.float32)
        base_sky = c_night * (1.0 - day_factor) + c_day * day_factor
        self.current_sky_color = base_sky * (1.0 - sunset_factor) + c_sunset * sunset_factor
        amb_day = np.array([0.6, 0.6, 0.65], dtype=np.float32)
        amb_night = np.array([0.15, 0.15, 0.2], dtype=np.float32)
        amb_sunset = np.array([0.35, 0.25, 0.45], dtype=np.float32) 
        base_amb = amb_night * (1.0 - day_factor) + amb_day * day_factor
        self.ambient_light = base_amb * (1.0 - sunset_factor) + amb_sunset * sunset_factor
        sun_fade = self.smoothstep(-0.05, 0.05, h)
        moon_h = -h
        moon_fade = self.smoothstep(0.1, 0.3, moon_h)
        if h > -0.05:
            self.light_dir = sun_vec
            sun_noon = np.array([1.0, 1.0, 0.9], dtype=np.float32)
            sun_gold = np.array([1.0, 0.8, 0.5], dtype=np.float32)
            sun_red = np.array([1.0, 0.3, 0.1], dtype=np.float32)
            if h > 0.15:
                blend = self.smoothstep(0.15, 0.4, h)
                current_sun_color = sun_gold * (1.0 - blend) + sun_noon * blend
            else:
                blend = self.smoothstep(-0.05, 0.15, h)
                current_sun_color = sun_red * (1.0 - blend) + sun_gold * blend
            self.light_color = current_sun_color
            self.light_intensity = sun_fade * (1.0 + sunset_factor * 0.1)
        else:
            self.light_dir = -sun_vec
            moon_color = np.array([0.5, 0.6, 0.9], dtype=np.float32)
            self.light_color = moon_color
            self.light_intensity = 0.4 * moon_fade
        self.current_container_ent = None
        px, py, pz = self.camera.pos
        center_y = py - self.player_height * 0.5
        nearby = self.get_nearby_entities(px, pz, radius=1, py=center_y)
        for ent in nearby:
            if ent.is_hole or ent.is_animating: continue
            if ent.density < 0.1: continue 
            min_p, max_p = ent.get_aabb()
            eps = 0.05
            if (px > min_p[0] + eps and px < max_p[0] - eps and
                center_y > min_p[1] + eps and center_y < max_p[1] - eps and
                pz > min_p[2] + eps and pz < max_p[2] - eps):
                self.current_container_ent = ent
                break
    def smoothstep(self, edge0, edge1, x):
        t = (x - edge0) / (edge1 - edge0)
        t = max(0.0, min(1.0, t))
        return t * t * (3.0 - 2.0 * t)
    def is_chunk_visible(self, cx, cy, cz, cam_pos=None):
        if cam_pos is None: cam_pos = self.camera.pos
        center_x = cx * self.CHUNK_SIZE + self.CHUNK_SIZE / 2.0
        center_y = cy * self.CHUNK_SIZE + self.CHUNK_SIZE / 2.0
        center_z = cz * self.CHUNK_SIZE + self.CHUNK_SIZE / 2.0
        dx = center_x - cam_pos[0]
        dy = center_y - cam_pos[1]
        dz = center_z - cam_pos[2]
        dist_sq = dx*dx + dy*dy + dz*dz
        if dist_sq < 625: 
            return True
        dist = math.sqrt(dist_sq)
        if dist < 0.001: return True
        dx /= dist; dy /= dist; dz /= dist
        fx, fy, fz = self.camera.front
        dot = dx*fx + dy*fy + dz*fz
        threshold = 0.4 if cam_pos is self.camera.pos else -0.5
        return dot > threshold
    def _draw_tool_slice_flash_modern(self):
        now = pygame.time.get_ticks()
        if (now - self.last_slice_time < 200) and (self.last_slice_pos is not None):
            p = self.last_slice_pos
            norm = self.last_slice_norm
            sz = 30.0
            col = (0.0, 1.0, 0.0, 0.3)
            if abs(norm[1]) > 0.9:   
                self.solid_renderer.add_cube(p, [sz, 0, sz], col)
            elif abs(norm[0]) > 0.9: 
                self.solid_renderer.add_cube(p, [0, sz, sz], col)
            elif abs(norm[2]) > 0.9: 
                self.solid_renderer.add_cube(p, [sz, sz, 0], col)
    def _render_chunks_modern(self, cull_pos=None, override_view=None, override_proj=None, skip_ent=None):
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_CULL_FACE)
        
        # --- ЛОГИКА МАТРИЦ ---
        if override_view is not None and override_proj is not None:
            # Это отражение (зеркало)
            view_mat = override_view
            proj_mat = override_proj
            glCullFace(GL_FRONT) # Для зеркал инвертируем грани
            
            # Позиция глаз для шейдера (зеркальная)
            shader_eye_pos = cull_pos if cull_pos is not None else self.camera.pos
        else:
            # Это основной вид (Глаза игрока)
            glCullFace(GL_BACK)
            
            aspect = self.draw_w / self.draw_h if self.draw_h > 0 else 1.0
            proj_mat = MatrixUtils.perspective(FOV, aspect, NEAR_CLIP, FAR_CLIP)
            
            # === СГЛАЖИВАНИЕ КАМЕРЫ ЗДЕСЬ ===
            # Создаем временную координату для рендера
            render_pos = np.copy(self.camera.pos)
            
            # Если мы в режиме приключения - подменяем высоту на плавную
            if not self.creative_mode:
                render_pos[1] = self.camera.visual_y
            
            # Строим матрицу взгляда от ПЛАВНОЙ позиции
            target = render_pos + self.camera.front
            view_mat = MatrixUtils.look_at(render_pos, target, np.array([0,1,0], dtype=np.float32))
            
            # Позиция глаз для шейдера (блики, туман) тоже плавная
            shader_eye_pos = render_pos
            
        self.shader.use()
        self.shader.set_mat4("projection", proj_mat)
        self.shader.set_mat4("view", view_mat)
        
        # ... (установка uniform-переменных) ...
        glUniform1f(glGetUniformLocation(self.shader.program, "uvScale"), UV_SCALE)
        loc_model = glGetUniformLocation(self.shader.program, "model")
        loc_useWorldUV = glGetUniformLocation(self.shader.program, "useWorldUV")
        glUniform1i(glGetUniformLocation(self.shader.program, "uTexMain"), 0)
        glActiveTexture(GL_TEXTURE1)
        glBindTexture(GL_TEXTURE_2D, self.noise_tex_id)
        glUniform1i(glGetUniformLocation(self.shader.program, "uTexNoise"), 1)
        loc_texType = glGetUniformLocation(self.shader.program, "uTexType")
        
        glUniform3f(glGetUniformLocation(self.shader.program, "sunDirection"), *self.light_dir)
        glUniform3f(glGetUniformLocation(self.shader.program, "sunColor"), *self.light_color)
        glUniform3f(glGetUniformLocation(self.shader.program, "ambientColor"), *self.ambient_light)
        glUniform1f(glGetUniformLocation(self.shader.program, "lightIntensity"), self.light_intensity)
        
        # Передаем правильную позицию глаз в шейдер
        glUniform3f(glGetUniformLocation(self.shader.program, "viewPos"), *shader_eye_pos)
        
        fog_end = self.slider_fog.value if hasattr(self, 'slider_fog') else 100.0
        fog_start = fog_end * 0.2
        glUniform1f(glGetUniformLocation(self.shader.program, "fogStart"), fog_start)
        glUniform1f(glGetUniformLocation(self.shader.program, "fogEnd"), fog_end)
        glUniform3f(glGetUniformLocation(self.shader.program, "fogColor"), *self.current_sky_color)
        
        # --- Свет ---
        num_active_lights = 0
        if not self.creative_mode: 
            visible_lights = self._collect_lights_optimized()
            has_lantern = (self.lantern_radius > 1.0) 
            if has_lantern:
                lamp_color = (1.0, 0.95, 0.8) 
                fixed_intensity = 0.9
                # Фонарик должен исходить из "плавных" глаз, иначе он будет дергаться
                lamp_pos = shader_eye_pos 
                player_lamp = (0.0, lamp_pos, lamp_color, fixed_intensity)
                visible_lights.insert(0, player_lamp)
            max_lights = 64
            if len(visible_lights) > max_lights:
                visible_lights = visible_lights[:max_lights]
            num_active_lights = len(visible_lights)
            for i, (dist, pos, color, intensity) in enumerate(visible_lights):
                base_name = f"pointLights[{i}]"
                glUniform3f(glGetUniformLocation(self.shader.program, f"{base_name}.position"), *pos)
                final_color = np.array(color) * intensity 
                if not (has_lantern and i == 0): final_color *= 2.0
                glUniform3f(glGetUniformLocation(self.shader.program, f"{base_name}.color"), *final_color)
                if has_lantern and i == 0:
                    r = max(1.0, self.lantern_radius) 
                    k_constant = 1.0; k_linear = 4.5 / r; k_quadratic = 75.0 / (r * r)
                    glUniform1f(glGetUniformLocation(self.shader.program, f"{base_name}.constant"), k_constant)
                    glUniform1f(glGetUniformLocation(self.shader.program, f"{base_name}.linear"), k_linear)
                    glUniform1f(glGetUniformLocation(self.shader.program, f"{base_name}.quadratic"), k_quadratic)
                else:
                    glUniform1f(glGetUniformLocation(self.shader.program, f"{base_name}.constant"), 1.0)
                    glUniform1f(glGetUniformLocation(self.shader.program, f"{base_name}.linear"), 0.14)
                    glUniform1f(glGetUniformLocation(self.shader.program, f"{base_name}.quadratic"), 0.07)
        glUniform1i(glGetUniformLocation(self.shader.program, "numLights"), num_active_lights)
        
        # --- ОТРИСОВКА HOLES (Stencil) ---
        glEnable(GL_STENCIL_TEST)
        glClear(GL_STENCIL_BUFFER_BIT) 
        glStencilFunc(GL_ALWAYS, 1, 0xFF)
        glStencilOp(GL_KEEP, GL_KEEP, GL_REPLACE)
        glColorMask(GL_FALSE, GL_FALSE, GL_FALSE, GL_FALSE)
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, self.texture_manager.get_white_texture())
        glUniform1i(loc_texType, 0) 
        glDepthMask(GL_FALSE)
        for ent in self.scene.entities:
            if ent.is_hole:
                m_scale = MatrixUtils.scale(ent.scale[0], ent.scale[1], ent.scale[2])
                m_trans = MatrixUtils.translation(ent.pos[0], ent.pos[1], ent.pos[2])
                model_mat = m_trans @ m_scale
                glUniformMatrix4fv(loc_model, 1, GL_TRUE, model_mat)
                self.cube_renderer.draw()
        glColorMask(GL_TRUE, GL_TRUE, GL_TRUE, GL_TRUE)
        glDepthMask(GL_TRUE)
        glStencilFunc(GL_NOTEQUAL, 1, 0xFF)
        glStencilOp(GL_KEEP, GL_KEEP, GL_KEEP)
        
        # --- ПОЛ (Floor) ---
        glUniformMatrix4fv(loc_model, 1, GL_TRUE, MatrixUtils.identity())
        glUniform1i(loc_useWorldUV, 1) 
        glUniform1i(loc_texType, 0)
        glEnable(GL_POLYGON_OFFSET_FILL)
        glPolygonOffset(1.0, 1.0)
        glDisable(GL_CULL_FACE)
        self.floor_renderer.draw()
        glEnable(GL_CULL_FACE)
        glDisable(GL_POLYGON_OFFSET_FILL)
        glUniform1i(loc_useWorldUV, 0)
        glDisable(GL_STENCIL_TEST)
        glUniformMatrix4fv(loc_model, 1, GL_TRUE, MatrixUtils.identity())
        
        # === ДВУХПРОХОДНЫЙ РЕНДЕРИНГ ЧАНКОВ ===
        visible_chunks = []
        # Для отсечения чанков используем ФИЗИЧЕСКУЮ позицию (чтобы геометрия не исчезала раньше времени)
        check_pos = cull_pos if cull_pos is not None else self.camera.pos
        
        for (cx, cy, cz), mesh_dict in self.chunk_meshes.items():
            if self.is_chunk_visible(cx, cy, cz, check_pos):
                visible_chunks.append(mesh_dict)
                
        render_r = 24 if self.creative_mode else 12
        r2 = render_r ** 2
        visible_large_ents_meshes = []
        visible_large_ents = self.get_visible_large_entities(r2 * 100)
        for ent in visible_large_ents:
            if skip_ent is not None and ent == skip_ent: continue
            if ent.uid in self.large_objects_gl_cache and not ent.is_animating:
                visible_large_ents_meshes.append(self.large_objects_gl_cache[ent.uid])

        # --- ПРОХОД 1: Непрозрачные (OPAQUE) ---
        glDepthMask(GL_TRUE)
        glDisable(GL_BLEND)
        
        def render_mesh_dict(mesh_dict, draw_transparent):
            for (tex_id, mode, is_trans), mesh in mesh_dict.items():
                if is_trans == draw_transparent:
                    glActiveTexture(GL_TEXTURE0)
                    glBindTexture(GL_TEXTURE_2D, tex_id)
                    glUniform1i(loc_texType, mode)
                    mesh.draw()

        for mesh_dict in visible_chunks:
            render_mesh_dict(mesh_dict, draw_transparent=False)
        for mesh_dict in visible_large_ents_meshes:
            render_mesh_dict(mesh_dict, draw_transparent=False)

        # --- ПРОХОД 2: Прозрачные (TRANSPARENT) ---
        glDepthMask(GL_FALSE)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        
        # Сортировка прозрачных
        px, py, pz = shader_eye_pos # Сортируем от текущего положения глаз
        sorted_chunks = []
        for (cx, cy, cz), mesh_dict in self.chunk_meshes.items():
            if self.is_chunk_visible(cx, cy, cz, check_pos):
                ccx = cx * self.CHUNK_SIZE + self.CHUNK_SIZE/2
                ccy = cy * self.CHUNK_SIZE + self.CHUNK_SIZE/2
                ccz = cz * self.CHUNK_SIZE + self.CHUNK_SIZE/2
                d2 = (ccx-px)**2 + (ccy-py)**2 + (ccz-pz)**2
                sorted_chunks.append((d2, mesh_dict))
        
        sorted_chunks.sort(key=lambda x: x[0], reverse=True)
        
        for _, mesh_dict in sorted_chunks:
            render_mesh_dict(mesh_dict, draw_transparent=True)
        for mesh_dict in visible_large_ents_meshes:
            render_mesh_dict(mesh_dict, draw_transparent=True)

        if self.current_container_ent:
            glDisable(GL_CULL_FACE)
            glUniformMatrix4fv(glGetUniformLocation(self.shader.program, "model"), 1, GL_TRUE, MatrixUtils.identity())
            glUniform1i(glGetUniformLocation(self.shader.program, "useWorldUV"), 0)
            self._render_specific_entity_internal(self.current_container_ent)
            glEnable(GL_CULL_FACE)
            
        glDisable(GL_BLEND)
        glDepthMask(GL_TRUE)
        glUseProgram(0)
    def _add_animated_door_geometry(self, solid_batch, trans_batch):
        for anim in self.door_animations:
            ent = anim['ent']
            pos = anim['original_pos']
            scale = anim['original_scale']
            pivot = anim['pivot']
            angle_deg = anim['current_angle']
            axis = anim['axis']
            dx, dy, dz = scale / 2.0
            cx, cy, cz = pos
            corners_orig = [
                np.array([cx - dx, cy - dy, cz + dz]), 
                np.array([cx + dx, cy - dy, cz + dz]), 
                np.array([cx + dx, cy + dy, cz + dz]), 
                np.array([cx - dx, cy + dy, cz + dz]), 
                np.array([cx - dx, cy - dy, cz - dz]), 
                np.array([cx + dx, cy - dy, cz - dz]), 
                np.array([cx + dx, cy + dy, cz - dz]), 
                np.array([cx - dx, cy + dy, cz - dz])  
            ]
            rad = math.radians(angle_deg)
            c = math.cos(rad)
            s = math.sin(rad)
            ux, uy, uz = axis
            rot_mat = np.array([
                [c + ux**2*(1-c),    ux*uy*(1-c) - uz*s, ux*uz*(1-c) + uy*s],
                [uy*ux*(1-c) + uz*s, c + uy**2*(1-c),    uy*uz*(1-c) - ux*s],
                [uz*ux*(1-c) - uy*s, uz*uy*(1-c) + ux*s, c + uz**2*(1-c)]
            ], dtype=np.float32)
            corners_rotated = []
            for p in corners_orig:
                vec = p - pivot
                rotated_vec = np.dot(rot_mat, vec)
                final_p = pivot + rotated_vec
                corners_rotated.append(final_p)
            c = corners_rotated
            faces_indices = [
                [1, 5, 6, 2], 
                [4, 0, 3, 7], 
                [3, 2, 6, 7], 
                [4, 5, 1, 0], 
                [0, 1, 2, 3], 
                [5, 4, 7, 6]  
            ]
            for i, indices in enumerate(faces_indices):
                color_data = ent.faces_colors[i]
                base_color = list(color_data[:4]) 
                if len(color_data) > 4:
                    emission = color_data[4]
                    if emission > 0:
                        base_color[0] = min(1.0, base_color[0] + emission * 0.5)
                        base_color[1] = min(1.0, base_color[1] + emission * 0.5)
                        base_color[2] = min(1.0, base_color[2] + emission * 0.5)
                target_batch = trans_batch if base_color[3] < 0.99 else solid_batch
                p0 = c[indices[0]]
                p1 = c[indices[1]]
                p2 = c[indices[2]]
                p3 = c[indices[3]]
                target_batch.vertices.extend([*p0, *base_color, *p1, *base_color, *p2, *base_color])
                target_batch.vertices.extend([*p0, *base_color, *p2, *base_color, *p3, *base_color])
    def draw_celestial_bodies(self, view_mat, proj_mat):
        dist = 400.0 
        rad_time = math.radians(self.sun_angle_time)
        rad_tilt = math.radians(self.sun_angle_tilt)
        rad_rot  = math.radians(self.sun_rotation_y) 
        base_x = math.cos(rad_time)
        base_y = math.sin(rad_time)
        base_z = math.tan(rad_tilt)
        c_rot = math.cos(rad_rot)
        s_rot = math.sin(rad_rot)
        final_x = base_x * c_rot - base_z * s_rot
        final_y = base_y
        final_z = base_x * s_rot + base_z * c_rot
        raw_sun_vec = np.array([final_x, final_y, final_z], dtype=np.float32)
        norm = np.linalg.norm(raw_sun_vec)
        if norm > 0: raw_sun_vec /= norm
        sun_pos = self.camera.pos + raw_sun_vec * dist
        moon_pos = self.camera.pos - raw_sun_vec * dist 
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glDisable(GL_DEPTH_TEST) 
        self.sprite_renderer.vertices.clear()
        self.sprite_renderer.add_billboard(
            sun_pos, 80, (1, 1, 1, 1), 
            self.camera.right, self.camera.up
        )
        self.sprite_renderer.flush(view_mat, proj_mat, self.tex_sun)
        self.sprite_renderer.add_billboard(
            moon_pos, 80, (1, 1, 1, 1), 
            self.camera.right, self.camera.up
        )
        self.sprite_renderer.flush(view_mat, proj_mat, self.tex_moon)
        glEnable(GL_DEPTH_TEST)
    def _render_frame(self, dt):
        # Рассчитываем плавную позицию камеры для неба и зеркал
        cam_pos_visual = np.copy(self.camera.pos)
        if not self.creative_mode:
            cam_pos_visual[1] = self.camera.visual_y
            
        cam_dir = self.camera.front
        limit_sq = 120.0 * 120.0
        
        # Список потенциальных зеркал: (dist_sq, ent, face_idx, axis, sign, is_animating_flag)
        potential_faces = []
        face_defs = [(0, 1.0), (0, -1.0), (1, 1.0), (1, -1.0), (2, 1.0), (2, -1.0)]
        
        for ent in self.scene.entities:
            # Оптимизация: проверяем наличие отражений
            if not hasattr(ent, 'faces_reflectivity'): continue
            if max(ent.faces_reflectivity) < 0.01: continue
            
            # Если объект анимируется - проверяем расстояние до его "оригинальной" позиции (упрощенно)
            # Если статика - до текущей
            check_pos = ent.pos
            if ent.is_animating:
                # Найти анимацию, чтобы взять pivot (примерно) или просто берем текущую pos, 
                # которая при анимации может быть старой, но для отсечения по дистанции сойдет
                pass

            vec_to_ent = check_pos - cam_pos
            d2_ent = np.sum(vec_to_ent**2)
            if d2_ent > limit_sq: continue
            
            for f_idx, (ax, sg) in enumerate(face_defs):
                if ent.faces_reflectivity[f_idx] > 0.01:
                    # Добавляем в список кандидатов
                    potential_faces.append((d2_ent, ent, ax, sg))

        potential_faces.sort(key=lambda x: x[0])
        
        active_mirrors_data = []
        
        for d2, m_ent, ax, sg in potential_faces:
            if len(active_mirrors_data) >= MAX_MIRRORS: break
            
            # --- ЛОГИКА АНИМИРОВАННОГО ЗЕРКАЛА ---
            override_point = None
            override_normal = None
            
            current_center = None
            u_vec = None
            v_vec = None
            
            if m_ent.is_animating:
                # 1. Ищем анимацию для этого энтити
                anim_data = next((a for a in self.door_animations if a['ent'] == m_ent), None)
                if anim_data:
                    # Рассчитываем матрицу
                    ang = anim_data['current_angle']
                    piv = anim_data['pivot']
                    axs = anim_data['axis']
                    rad = math.radians(ang)
                    c = math.cos(rad); s = math.sin(rad)
                    ux, uy, uz = axs
                    rot_mat = np.array([
                        [c + ux**2*(1-c),    ux*uy*(1-c) - uz*s, ux*uz*(1-c) + uy*s],
                        [uy*ux*(1-c) + uz*s, c + uy**2*(1-c),    uy*uz*(1-c) - ux*s],
                        [uz*ux*(1-c) - uy*s, uz*uy*(1-c) + ux*s, c + uz**2*(1-c)]
                    ], dtype=np.float32)
                    
                    # 2. Рассчитываем нормаль
                    base_normal = np.zeros(3); base_normal[ax] = sg
                    dynamic_normal = np.dot(rot_mat, base_normal)
                    override_normal = dynamic_normal
                    
                    # 3. Рассчитываем точку на плоскости (центр грани)
                    # Берем исходный центр грани относительно pivot
                    orig_pos = anim_data['original_pos']
                    orig_scale = anim_data['original_scale']
                    
                    base_offset = np.zeros(3); base_offset[ax] = (orig_scale[ax] / 2.0) * sg
                    orig_face_center = orig_pos + base_offset
                    
                    vec = orig_face_center - piv
                    rot_vec = np.dot(rot_mat, vec)
                    dynamic_center = piv + rot_vec
                    override_point = dynamic_center
                    
                    current_center = dynamic_center
                    
                    # Для проверки видимости (check_points) нужно знать оси U и V грани
                    # И их тоже нужно повернуть!
                    axes_indices = [0, 1, 2]; axes_indices.remove(ax)
                    ua, va = axes_indices
                    
                    vec_u = np.zeros(3); vec_u[ua] = 1.0
                    vec_v = np.zeros(3); vec_v[va] = 1.0
                    
                    u_vec = np.dot(rot_mat, vec_u) * (orig_scale[ua] * 0.4)
                    v_vec = np.dot(rot_mat, vec_v) * (orig_scale[va] * 0.4)
            else:
                # Статика
                current_center = m_ent.pos.copy()
                current_center[ax] += (m_ent.scale[ax] / 2.0) * sg
                
                axes_indices = [0, 1, 2]; axes_indices.remove(ax)
                ua, va = axes_indices
                u_vec = np.zeros(3); u_vec[ua] = m_ent.scale[ua] * 0.4
                v_vec = np.zeros(3); v_vec[va] = m_ent.scale[va] * 0.4
                
                normal_check = np.zeros(3); normal_check[ax] = sg
                # Простая проверка: если грань отвернута от камеры
                to_face = current_center - cam_pos
                if np.dot(to_face, normal_check) > 0: continue

            # --- Проверка видимости (Raycast 5 точек) ---
            check_points = [current_center]
            for du, dv in [(1, 1), (1, -1), (-1, 1), (-1, -1)]:
                pt = current_center + u_vec * du + v_vec * dv
                check_points.append(pt)
            
            is_visible = False
            for test_pt in check_points:
                vec = test_pt - cam_pos
                dst = np.linalg.norm(vec)
                if dst < 0.001: continue
                r_dir = vec / dst
                
                cands = self.get_candidates_for_ray(cam_pos, r_dir, max_dist=dst + 1.0)
                hit, hd, _ = self.scene.raycast(cam_pos, r_dir, ignore_holes=True, candidates=cands)
                
                # Если видим точку (hit == m_ent или hit == None или hit дальше зеркала)
                if hit is None or hit == m_ent or hd >= dst - 0.15:
                    is_visible = True
                    break
            
            if is_visible:
                # Добавляем данные для рендера (entity, axis, sign, override_pt, override_norm)
                active_mirrors_data.append((m_ent, ax, sg, override_point, override_normal))

        reflection_mode = 0
        if active_mirrors_data:
            reflection_mode = 1
            for i, (m_ent, axis, sign, ov_p, ov_n) in enumerate(active_mirrors_data):
                self._render_reflection_pass(m_ent, self.reflection_fbos[i], axis, sign, ov_p, ov_n)

        # --- Основной рендер ---
        glClearColor(*self.current_sky_color, 1.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT | GL_STENCIL_BUFFER_BIT)
        
        aspect = self.draw_w / self.draw_h if self.draw_h > 0 else 1.0
        proj_mat = MatrixUtils.perspective(FOV, aspect, NEAR_CLIP, FAR_CLIP)
        
        # СТРОИМ МАТРИЦУ ДЛЯ НЕБА И ОБЛАКОВ, ИСПОЛЬЗУЯ ПЛАВНУЮ ПОЗИЦИЮ
        target = cam_pos_visual + self.camera.front
        view_mat = MatrixUtils.look_at(cam_pos_visual, target, np.array([0,1,0], dtype=np.float32))
        
        self.shader.use()
        self.shader.set_mat4("projection", proj_mat)
        self.shader.set_mat4("view", view_mat)
        glUniform4f(glGetUniformLocation(self.shader.program, "uClipPlane"), 0, 0, 0, 0)
        
        glUniform1i(glGetUniformLocation(self.shader.program, "uReflectionMode"), reflection_mode)
        
        if reflection_mode == 1:
            glUniform1i(glGetUniformLocation(self.shader.program, "uActiveMirrors"), len(active_mirrors_data))
            glUniform2f(glGetUniformLocation(self.shader.program, "uWindowSize"), float(self.draw_w), float(self.draw_h))
            
            for i, (m_ent, axis, sign, ov_p, ov_n) in enumerate(active_mirrors_data):
                slot = 2 + i
                glActiveTexture(GL_TEXTURE0 + slot)
                glBindTexture(GL_TEXTURE_2D, self.reflection_fbos[i].tex)
                glUniform1i(glGetUniformLocation(self.shader.program, f"uTexReflections[{i}]"), slot)
                
                # Передаем координаты зеркала шейдеру
                if ov_p is not None and ov_n is not None:
                    glUniform3f(glGetUniformLocation(self.shader.program, f"uMirrorPos[{i}]"), *ov_p)
                    glUniform3f(glGetUniformLocation(self.shader.program, f"uMirrorNormal[{i}]"), *ov_n)
                else:
                    norm_vec = np.zeros(3); norm_vec[axis] = sign
                    pt = m_ent.pos.copy(); pt[axis] += (m_ent.scale[axis]/2.0)*sign
                    glUniform3f(glGetUniformLocation(self.shader.program, f"uMirrorPos[{i}]"), *pt)
                    glUniform3f(glGetUniformLocation(self.shader.program, f"uMirrorNormal[{i}]"), *norm_vec)

        self.star_renderer.draw(view_mat, proj_mat, cam_pos_visual, self.sun_angle_time, self.sun_angle_tilt, self.sun_rotation_y, self.light_intensity)
        self.draw_celestial_bodies(view_mat, proj_mat)
        
        self.update_chunks()
        
        # Вызываем рендер чанков (он сам возьмет visual_y внутри, так как мы обновили его выше)
        self._render_chunks_modern()
        
        # Рисуем двери (основной проход)
        if self.door_animations:
             door_batches = self._generate_lit_door_geometry()
             self.shader.use() 
             glUniform4f(glGetUniformLocation(self.shader.program, "uClipPlane"), 0, 0, 0, 0) 
             glEnable(GL_BLEND); glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
             for (tex_id, mode), data_array in door_batches.items():
                if len(data_array) == 0: continue
                glActiveTexture(GL_TEXTURE0); glBindTexture(GL_TEXTURE_2D, tex_id)
                glUniform1i(glGetUniformLocation(self.shader.program, "uTexType"), mode)
                glDepthMask(True)
                mesh = MeshBuffer(data_array)
                mesh.draw()
                mesh.delete()
             glDisable(GL_BLEND)
             
        fog_val = self.fog_distance if hasattr(self, 'fog_distance') else 100.0
        self.cloud_renderer.draw(view_mat, proj_mat, cam_pos_visual, self.light_color, self.light_intensity, dt, fog_val)
        
        if self.creative_mode:
            pass

            ray_o, ray_d = self.get_world_ray()
            glEnable(GL_DEPTH_TEST)
            glDepthMask(False) 
            glEnable(GL_BLEND); glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
            self.line_renderer.vertices.clear()

            grid_inner_r = 10.0
            grid_outer_r = 30.0
            safe_radius = int(grid_outer_r)
            step = 1
            px, py, pz = self.camera.pos
            base_x = round(px / step) * step
            base_z = round(pz / step) * step
            grid_y = 0.015
            rgb = [0.3, 0.3, 0.3]
            base_alpha = 0.4
            dist_y = abs(py - grid_y)
            def get_faded_color(dist_3d):
                if dist_3d <= grid_inner_r: return base_alpha
                if dist_3d >= grid_outer_r: return 0.0
                return base_alpha * (1.0 - (dist_3d - grid_inner_r) / (grid_outer_r - grid_inner_r))
            if dist_y < grid_outer_r:
                for i in range(0, safe_radius + 1, step):
                    dist_3d = math.sqrt(i*i + dist_y*dist_y)
                    alpha = get_faded_color(dist_3d)
                    if alpha <= 0.0: 
                        if i == 0: break 
                        continue
                    offset_xs = [base_x + i]; offset_zs = [base_z + i]
                    if i != 0: offset_xs.append(base_x - i); offset_zs.append(base_z - i)
                    v_center = [*rgb, alpha]
                    v_edge = [*rgb, 0.0] 
                    for x in offset_xs: 
                        self.line_renderer.vertices.extend([x, grid_y, base_z, *v_center, x, grid_y, base_z + safe_radius, *v_edge])
                        self.line_renderer.vertices.extend([x, grid_y, base_z, *v_center, x, grid_y, base_z - safe_radius, *v_edge])
                    for z in offset_zs: 
                        self.line_renderer.vertices.extend([base_x, grid_y, z, *v_center, base_x + safe_radius, grid_y, z, *v_edge])
                        self.line_renderer.vertices.extend([base_x, grid_y, z, *v_center, base_x - safe_radius, grid_y, z, *v_edge])
            self.line_renderer.flush(view_mat, proj_mat, line_width=1.0)
            glDepthMask(True)
            glEnable(GL_DEPTH_TEST)
            self.line_renderer.vertices.clear()
            self.sprite_renderer.vertices.clear()
            if self.selected_entities:
                yellow_col = (1.0, 1.0, 0.0, 0.5)
                blue_col = (0.2, 0.6, 1.0, 0.9)
                for ent in self.selected_entities:
                    min_p, max_p = ent.get_aabb()
                    epsilon = 0.006
                    self.line_renderer.add_box(min_p - epsilon, max_p + epsilon, color=(1.0, 1.0, 0.0, 1.0))
                    selected_face_indices = self.selected_faces.get(ent, set())
                    for face_idx in range(6):
                        col = blue_col if face_idx in selected_face_indices else yellow_col
                        self._draw_aligned_face_grid(ent, face_idx, col)
            self.line_renderer.flush(view_mat, proj_mat, line_width=3.0)
            glDepthMask(False)
            glEnable(GL_BLEND)
            self.sprite_renderer.flush(view_mat, proj_mat, 0, mode=2)
            glDepthMask(True)
            self._draw_tool_visuals_modern(view_mat, proj_mat)
        
        glEnable(GL_BLEND); glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glDepthMask(False)
        self.sprite_renderer.flush(view_mat, proj_mat, 0, mode=1)
        glDepthMask(True)
        glUseProgram(0)
        
        if self.state == "CINECAM" and not self.is_rendering_video:
            glEnable(GL_DEPTH_TEST)
            self.cine_cam.render_world(view_mat, proj_mat, cam_pos)
            
        self.render_ui()
    def _draw_aligned_face_grid(self, ent, face_idx, color):
        offset = 0.005 
        min_p, max_p = ent.get_aabb()
        center = (min_p + max_p) / 2.0
        scale = max_p - min_p
        p1, p2, p3, p4 = None, None, None, None
        sx, sy, sz = scale[0]/2, scale[1]/2, scale[2]/2
        if face_idx == 0: 
            x = max_p[0] + offset
            p1=[x, min_p[1], max_p[2]]; p2=[x, min_p[1], min_p[2]]
            p3=[x, max_p[1], min_p[2]]; p4=[x, max_p[1], max_p[2]]
            uvs = [(sz, -sy), (-sz, -sy), (-sz, sy), (sz, sy)]
        elif face_idx == 1: 
            x = min_p[0] - offset
            p1=[x, min_p[1], min_p[2]]; p2=[x, min_p[1], max_p[2]]
            p3=[x, max_p[1], max_p[2]]; p4=[x, max_p[1], min_p[2]]
            uvs = [(-sz, -sy), (sz, -sy), (sz, sy), (-sz, sy)]
        elif face_idx == 2: 
            y = max_p[1] + offset
            p1=[min_p[0], y, max_p[2]]; p2=[max_p[0], y, max_p[2]]
            p3=[max_p[0], y, min_p[2]]; p4=[min_p[0], y, min_p[2]]
            uvs = [(-sx, sz), (sx, sz), (sx, -sz), (-sx, -sz)]
        elif face_idx == 3: 
            y = min_p[1] - offset
            p1=[min_p[0], y, min_p[2]]; p2=[max_p[0], y, min_p[2]]
            p3=[max_p[0], y, max_p[2]]; p4=[min_p[0], y, max_p[2]]
            uvs = [(-sx, -sz), (sx, -sz), (sx, sz), (-sx, sz)]
        elif face_idx == 4: 
            z = max_p[2] + offset
            p1=[min_p[0], min_p[1], z]; p2=[max_p[0], min_p[1], z]
            p3=[max_p[0], max_p[1], z]; p4=[min_p[0], max_p[1], z]
            uvs = [(-sx, -sy), (sx, -sy), (sx, sy), (-sx, sy)]
        elif face_idx == 5: 
            z = min_p[2] - offset
            p1=[max_p[0], min_p[1], z]; p2=[min_p[0], min_p[1], z]
            p3=[min_p[0], max_p[1], z]; p4=[max_p[0], max_p[1], z]
            uvs = [(sx, -sy), (-sx, -sy), (-sx, sy), (sx, sy)]
        if p1:
            self.sprite_renderer.add_quad_uv(p1, p2, p3, p4, uvs, color)
    def draw_guide_plane_modern(self, center, axis):
        grid_sz = 50.0
        x, y, z = center
        col = (1.0, 1.0, 1.0, 0.15)
        epsilon = 0.005 
        if axis == 1: 
            self.solid_renderer.add_cube([x, y + epsilon, z], [grid_sz*2, 0, grid_sz*2], col)
        elif axis == 0: 
            self.solid_renderer.add_cube([x + epsilon, y, z], [0, grid_sz*2, grid_sz*2], col)
        elif axis == 2: 
            self.solid_renderer.add_cube([x, y, z + epsilon], [grid_sz*2, grid_sz*2, 0], col)
    def _draw_tool_visuals_modern(self, view_mat, proj_mat):
        self._queue_creative_visuals()
        ray_o, ray_d = self.get_world_ray()
        glEnable(GL_DEPTH_TEST)
        glDepthMask(False) 
        glEnable(GL_BLEND); glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        if self.tool_mode == 'SLICE': 
            self._draw_tool_slice_preview(ray_o, ray_d)
        elif self.tool_mode == 'CUBE':
            # Для визуализации используем логику Place (ЛКМ), так курсор всегда виден на поверхности
            c_size, c_center, _, _ = self._get_cube_tool_data(ray_o, ray_d, is_cutting=False)
            
            if c_center is not None:
                self.solid_renderer.add_cube(c_center, c_size, (0.0, 1.0, 0.0, 0.3))
                min_p = c_center - c_size/2
                max_p = c_center + c_size/2
                self.line_renderer.add_box(min_p, max_p, (0.0, 1.0, 0.0, 1.0))
                self.draw_measurements(min_p, max_p, max_p, show_components=True)
        self._draw_tool_slice_flash_modern()
        self.solid_renderer.flush(view_mat, proj_mat)
        self.line_renderer.flush(view_mat, proj_mat, line_width=2.0)
        glDisable(GL_DEPTH_TEST)
        is_extruding_box = (self.tool_mode == 'BOX' and self.box_extruding)
        is_extruding_room = (self.tool_mode == 'ROOM' and self.room_extruding)
        if is_extruding_box or is_extruding_room:
            base_rect = self.box_base_rect if is_extruding_box else self.room_base_rect
            ext_val = self.calculate_extrusion_height_generic(ray_o, ray_d, base_rect)
            p1, p2 = base_rect['p1'], base_rect['p2']
            axis = self.constraint_axis
            p_min, p_max = np.minimum(p1, p2), np.maximum(p1, p2)
            base_center = (p_min + p_max)/2.0
            base_size = p_max - p_min
            final_center = base_center.copy()
            final_center[axis] += ext_val / 2.0
            final_size = base_size.copy()
            final_size[axis] = abs(ext_val)
            if final_size[axis] < 0.01: final_size[axis] = 0.01
            temp_ent = Entity(final_center, final_size)
            col_fill = (0.0, 1.0, 1.0, 0.4)
            col_line = COLOR_PREVIEW
            self.solid_renderer.add_cube(temp_ent.pos, temp_ent.scale, col_fill)
            min_p, max_p = temp_ent.get_aabb()
            self.line_renderer.add_box_with_diagonals(min_p, max_p, col_line)
            self.draw_guide_plane_modern(self.build_start, axis)
            self.draw_measurements(min_p, max_p, max_p)
        else:
            curr = self.get_smart_cursor(ray_o, ray_d)
            if self.tool_mode == 'DOOR_CREATOR':
                corners_s = [[-1, 1, 1], [1, 1, 1], [1, -1, 1], [-1, -1, 1], [-1, 1, -1], [1, 1, -1], [1, -1, -1], [-1, -1, -1]]
                edges_idx = [(0, 1), (1, 2), (2, 3), (3, 0), (4, 5), (5, 6), (6, 7), (7, 4), (0, 4), (1, 5), (2, 6), (3, 7)]
                for e in self.scene.entities:
                    if e.is_door and e.hinge_edge != -1:
                        s, end = edges_idx[e.hinge_edge]
                        half = e.scale / 2.0
                        p1 = e.pos + np.array(corners_s[s]) * half
                        p2 = e.pos + np.array(corners_s[end]) * half
                        self.line_renderer.add_line(p1, p2, (0.8, 0.0, 1.0, 1.0))
                target_ent = self.highlighted_ent if self.door_tool_state == 'LOCKED' else None
                if self.door_tool_state != 'LOCKED':
                    cands = self.get_candidates_for_ray(ray_o, ray_d)
                    target_ent, _, _ = self.scene.raycast(ray_o, ray_d, candidates=cands)
                if target_ent:
                    self.highlighted_ent = target_ent
                    d_hit, pt_hit, _ = ray_aabb_intersect(ray_o, ray_d, *target_ent.get_aabb())
                    hit_p = pt_hit if pt_hit is not None else target_ent.pos
                    edge_idx = self.locked_hinge_edge if self.door_tool_state == 'LOCKED' else -1
                    if self.door_tool_state == 'HOVER':
                         if not target_ent.is_door:
                             edge_idx, _, _ = self.get_closest_edge_info(target_ent, hit_p)
                             self.temp_hinge_edge = edge_idx
                         else:
                             self.temp_hinge_edge = -1
                    if edge_idx != -1:
                        s, end = edges_idx[edge_idx]
                        half = target_ent.scale / 2.0
                        p1 = target_ent.pos + np.array(corners_s[s]) * half
                        p2 = target_ent.pos + np.array(corners_s[end]) * half
                        col = (1.0, 0.0, 0.0, 1.0) if self.door_tool_state == 'LOCKED' else (0.6, 0.0, 1.0, 1.0)
                        self.line_renderer.add_line(p1, p2, col)
            elif self.tool_mode in ['WALL', 'BOX', 'ROOM']:
                if curr is not None and self.build_start is not None:
                     self.line_renderer.add_line(self.build_start, curr, (0, 1, 1, 1))
                if curr is not None and self.build_start is None:
                     cands = self.get_candidates_for_ray(ray_o, ray_d)
                     hit_ent, _, hit_norm = self.scene.raycast(ray_o, ray_d, ignore_holes=True, candidates=cands)
                     if hit_ent and hit_norm is not None:
                         self._draw_entity_edge_distances(hit_ent, curr, hit_norm)
                col_fill = (0.0, 1.0, 1.0, 0.4)
                col_line = COLOR_PREVIEW
                if self.build_start is not None:
                    self.draw_guide_plane_modern(self.build_start, self.constraint_axis)
                    if curr is not None:
                        center = (self.build_start + curr) / 2.0
                        scale = np.abs(self.build_start - curr)
                        if self.tool_mode == 'WALL': scale = np.maximum(scale, 0.02)
                        else:
                            norm_axis = np.argmax(np.abs(self.build_normal))
                            if scale[norm_axis] < 0.05: scale[norm_axis] = 0.01 
                        temp_ent = Entity(center, scale)
                        self.solid_renderer.add_cube(temp_ent.pos, temp_ent.scale, col_fill)
                        min_p, max_p = temp_ent.get_aabb()
                        self.line_renderer.add_box_with_diagonals(min_p, max_p, col_line)
                        self.draw_measurements(min_p, max_p, max_p)
            elif self.tool_mode == 'CUT':
                keys = self.input.get_keys()
                is_ctrl = keys.get(sdl2.SDLK_LCTRL) or keys.get(sdl2.SDLK_RCTRL)
                current_snap = 0.01 if is_ctrl else self.snap_unit
                if self.cut_start_point is not None:
                    if self.cut_target_ent is not None:
                        curr_raw = self.get_point_on_plane(ray_o, ray_d, self.cut_start_point, self.cut_normal)
                        if curr_raw is not None:
                            curr = snap_vector(curr_raw, current_snap)
                            p1 = self.cut_start_point; p2 = curr
                            center = (p1 + p2) / 2
                            dims = np.abs(p1 - p2)
                            draw_dims = np.maximum(dims, 0.01)
                            axis = np.argmax(np.abs(self.cut_normal))
                            draw_dims[axis] = 0.002
                            bias = self.cut_normal * 0.005 
                            self.solid_renderer.add_cube(center + bias, draw_dims, (1.0, 0.0, 0.0, 0.4))
                            min_p = center - draw_dims/2
                            max_p = center + draw_dims/2
                            self.line_renderer.add_box(min_p + bias, max_p + bias, (1, 0, 0, 1))
                            self.draw_measurements(min_p, max_p, max_p)
                    else:
                        curr_raw = self.get_ground_intersect(ray_o, ray_d)
                        if curr_raw is not None:
                            curr = snap_vector(curr_raw, current_snap)
                            p1 = self.cut_start_point; p2 = curr
                            center = (p1 + p2) / 2.0; center[1] = 0.005
                            size = np.abs(p1 - p2); size[1] = 0.0
                            self.solid_renderer.add_cube(center, size, (1.0, 0.0, 0.0, 0.4))
                            min_p = center - size/2; max_p = center + size/2
                            self.line_renderer.add_box(min_p, max_p, (1, 0, 0, 1))
                            self.draw_measurements(min_p, max_p, max_p)
                elif curr is not None:
                    cands = self.get_candidates_for_ray(ray_o, ray_d)
                    ent, _, norm = self.scene.raycast(ray_o, ray_d, ignore_holes=True, candidates=cands)
                    if ent and norm is not None:
                        sz = 0.05
                        min_p = curr - sz/2; max_p = curr + sz/2
                        bias = norm * 0.005
                        self.line_renderer.add_box(min_p + bias, max_p + bias, (1, 0.5, 0, 1))
                        self._draw_entity_edge_distances(ent, curr, norm)
                    elif self.get_ground_intersect(ray_o, ray_d) is not None:
                        sz = 0.05
                        bias = np.array([0, 0.005, 0])
                        min_p = curr - sz/2; max_p = curr + sz/2
                        self.line_renderer.add_box(min_p + bias, max_p + bias, (1, 0.5, 0, 1))
            elif self.tool_mode == 'STRIP':
                if not self.strip_extruding:
                    cands = self.get_candidates_for_ray(ray_o, ray_d)
                    hit_ent, _, hit_norm = self.scene.raycast(ray_o, ray_d, ignore_holes=True, candidates=cands)
                    if hit_ent and hit_norm is not None and curr is not None:
                        self._draw_entity_edge_distances(hit_ent, curr, hit_norm)
                line_offset = self.strip_normal * 0.005 if self.strip_normal is not None else np.array([0.,0.,0.])
                if len(self.strip_points) > 0:
                    p0 = self.strip_points[0]; sz = 0.01
                    self.line_renderer.add_box(p0-sz, p0+sz, (1, 0, 1, 1))
                    for i in range(len(self.strip_points) - 1):
                        v1 = self.strip_points[i] + line_offset; v2 = self.strip_points[i+1] + line_offset
                        self.line_renderer.add_line(v1, v2, (0, 1, 1, 1))
                    if not self.strip_extruding and self.strip_plane_p is not None:
                        plane_hit = self.get_point_on_plane(ray_o, ray_d, self.strip_plane_p, self.strip_normal)
                        if plane_hit is not None:
                            keys = self.input.get_keys()
                            is_ctrl = keys.get(sdl2.SDLK_LCTRL) or keys.get(sdl2.SDLK_RCTRL)
                            snap = 0.01 if is_ctrl else self.snap_unit
                            curr = snap_vector(plane_hit, snap)
                            last_p = self.strip_points[-1]
                            start_p = self.strip_points[0]
                            dist_to_start_raw = np.linalg.norm(curr - start_p)
                            magnet_active = (dist_to_start_raw < 0.1) and (not is_ctrl)
                            final_p = None; corner_p = None
                            norm_axis = np.argmax(np.abs(self.strip_normal))
                            if magnet_active:
                                final_p = start_p
                                vec_to_start = start_p - last_p; vec_to_start[norm_axis] = 0
                                dom_axis = np.argmax(np.abs(vec_to_start))
                                is_diagonal = False
                                for i in range(3):
                                    if i != dom_axis and i != norm_axis:
                                        if abs(vec_to_start[i]) > 0.001: is_diagonal = True
                                if is_diagonal:
                                    corner_p = last_p.copy(); corner_p[dom_axis] = start_p[dom_axis]
                            else:
                                diff = curr - last_p; diff[norm_axis] = 0
                                dom_axis = np.argmax(np.abs(diff))
                                final_p = last_p.copy(); final_p[dom_axis] = curr[dom_axis]
                            if corner_p is not None:
                                self.line_renderer.add_line(last_p + line_offset, corner_p + line_offset, (1, 1, 0, 1))
                                self.line_renderer.add_line(corner_p + line_offset, final_p + line_offset, (1, 1, 0, 1))
                                self.draw_measurements(last_p, corner_p, corner_p, show_components=False)
                            else:
                                self.line_renderer.add_line(last_p + line_offset, final_p + line_offset, (1, 1, 0, 1))
                                if not magnet_active:
                                    self.draw_measurements(last_p, final_p, final_p, show_components=False)
                if self.strip_extruding and len(self.strip_points) >= 2:
                    axis = np.argmax(np.abs(self.strip_normal))
                    base_p = self.strip_points[-1]
                    h = self.calculate_extrusion_height_generic(ray_o, ray_d, base_p)
                    thickness = self.default_thickness
                    num_segments = len(self.strip_points) - 1
                    total_min = np.array([np.inf]*3); total_max = np.array([-np.inf]*3)
                    is_closed = (np.linalg.norm(self.strip_points[-1] - self.strip_points[0]) < 0.001)
                    for i in range(num_segments):
                        p_start = self.strip_points[i]; p_end = self.strip_points[i+1]
                        vec = p_end - p_start; length = np.linalg.norm(vec)
                        if length < 0.001: continue
                        direction = vec / length
                        extend_start = not (i == 0 and not is_closed)
                        extend_end = not (i == num_segments - 1 and not is_closed)
                        p_start_ext = p_start.copy()
                        p_end_ext = p_end.copy()
                        if extend_start: p_start_ext -= direction * (thickness / 2.0)
                        if extend_end: p_end_ext += direction * (thickness / 2.0)
                        center = (p_start_ext + p_end_ext) / 2.0
                        center[axis] += h / 2.0
                        size = np.array([thickness, thickness, thickness])
                        size[axis] = abs(h) if abs(h) > 0.01 else 0.01
                        seg_axis = np.argmax(np.abs(vec))
                        size[seg_axis] = np.linalg.norm(p_end_ext - p_start_ext)
                        self.solid_renderer.add_cube(center, size, (0.0, 1.0, 1.0, 0.4))
                        temp_min = center - size/2; temp_max = center + size/2
                        self.line_renderer.add_box_with_diagonals(temp_min, temp_max, COLOR_PREVIEW)
                        total_min = np.minimum(total_min, temp_min)
                        total_max = np.maximum(total_max, temp_max)
                    if total_min[0] != np.inf:
                        self.draw_measurements(total_min, total_max, total_max)
            elif self.tool_mode == 'SELECT':
                if self.selected_entities:
                    all_selected_faces = []
                    for ent, faces in self.selected_faces.items():
                        for f_idx in faces: all_selected_faces.append((ent, f_idx))
                    if len(all_selected_faces) == 2:
                        ent1, face1 = all_selected_faces[0]; ent2, face2 = all_selected_faces[1]
                        p1 = self.get_face_center_point(ent1, face1)
                        p2 = self.get_face_center_point(ent2, face2)
                        p_min = np.minimum(p1, p2); p_max = np.maximum(p1, p2)
                        self.draw_measurements(p_min, p_max, p_max)
                    else:
                        ent = self.selected_entities[-1]
                        min_p, max_p = ent.get_aabb()
                        ray_o, ray_d = self.get_world_ray()
                        dist, hit_point, _ = ray_aabb_intersect(ray_o, ray_d, min_p, max_p)
                        if hit_point is not None: 
                            cursor_p = hit_point
                        else:
                            smart_p = self.get_smart_cursor(ray_o, ray_d)
                            cursor_p = np.clip(smart_p, min_p, max_p) if smart_p is not None else max_p
                        self.draw_measurements(min_p, max_p, cursor_p)
        self.solid_renderer.flush(view_mat, proj_mat)
        self.line_renderer.flush(view_mat, proj_mat, line_width=2.0)
        glEnable(GL_DEPTH_TEST)
        glDepthMask(True)
        glDisable(GL_BLEND)
    def _draw_tool_slice_preview(self, ray_o, ray_d):
        if self.edit_mode: return 
        cands = self.get_candidates_for_ray(ray_o, ray_d)
        ent, dist, norm = self.scene.raycast(ray_o, ray_d, candidates=cands)
        if ent:
            raw_hit_p = ray_o + ray_d * dist
            keys = self.input.get_keys()
            snap = 0.01 if (keys.get(sdl2.SDLK_LCTRL) or keys.get(sdl2.SDLK_RCTRL)) else self.snap_unit
            hit_p = snap_vector(raw_hit_p, snap)
            slice_norm = np.array([0.0, 1.0, 0.0])
            is_floor = (norm is not None and abs(norm[1]) > 0.5)
            if is_floor:
                 if self.slice_orientation == 0: slice_norm = np.array([1.0, 0.0, 0.0])
                 else: slice_norm = np.array([0.0, 0.0, 1.0])
            else:
                if self.slice_orientation == 0:
                    if norm is not None:
                        if abs(norm[0]) > 0.5: slice_norm = np.array([0.0, 0.0, 1.0])
                        elif abs(norm[2]) > 0.5: slice_norm = np.array([1.0, 0.0, 0.0])
                else: slice_norm = np.array([0.0, 1.0, 0.0])
            sz = 30.0
            col = (1.0, 0.0, 0.0, 0.15)
            if abs(slice_norm[1]) > 0.9:   self.solid_renderer.add_cube(hit_p, [sz, 0, sz], col)
            elif abs(slice_norm[0]) > 0.9: self.solid_renderer.add_cube(hit_p, [0, sz, sz], col)
            elif abs(slice_norm[2]) > 0.9: self.solid_renderer.add_cube(hit_p, [sz, sz, 0], col)
            measure_axis = np.argmax(np.abs(slice_norm))
            half = ent.scale / 2.0
            min_pos = ent.pos - half
            max_pos = ent.pos + half
            p_min_edge = hit_p.copy(); p_min_edge[measure_axis] = min_pos[measure_axis]
            p_max_edge = hit_p.copy(); p_max_edge[measure_axis] = max_pos[measure_axis]
            vis_offset = np.array([0.01, 0.01, 0.01])
            yellow_col = (1.0, 1.0, 0.0, 1.0)
            self.line_renderer.add_line(p_min_edge + vis_offset, hit_p + vis_offset, yellow_col)
            self.line_renderer.add_line(hit_p + vis_offset, p_max_edge + vis_offset, yellow_col)
            dist1 = abs(hit_p[measure_axis] - min_pos[measure_axis])
            dist2 = abs(hit_p[measure_axis] - max_pos[measure_axis])
            mid1 = (p_min_edge + hit_p) / 2.0
            mid2 = (hit_p + p_max_edge) / 2.0
            text_offset = (0, -20)
            self.queue_label_at(mid1 + vis_offset, f"{dist1:.2f}", (1.0, 1.0, 0.0), text_offset)
            self.queue_label_at(mid2 + vis_offset, f"{dist2:.2f}", (1.0, 1.0, 0.0), text_offset)
    def _draw_entity_edge_distances(self, ent, curr, norm):
        if not hasattr(self, 'aux_labels'):
            self.aux_labels = [TextLabel(self.font, (255, 255, 0)) for _ in range(4)]
        norm_axis = np.argmax(np.abs(norm))
        if norm_axis == 0:   a1, a2 = 2, 1 
        elif norm_axis == 1: a1, a2 = 0, 2 
        else:                a1, a2 = 0, 1 
        half = ent.scale / 2.0
        min_pos = ent.pos - half
        max_pos = ent.pos + half
        offset_vec = norm * 0.01
        col = (1, 1, 0, 0.7) 
        p_a1_min = curr.copy(); p_a1_min[a1] = min_pos[a1]
        self.line_renderer.add_line(curr + offset_vec, p_a1_min + offset_vec, col)
        p_a1_max = curr.copy(); p_a1_max[a1] = max_pos[a1]
        self.line_renderer.add_line(curr + offset_vec, p_a1_max + offset_vec, col)
        p_a2_min = curr.copy(); p_a2_min[a2] = min_pos[a2]
        self.line_renderer.add_line(curr + offset_vec, p_a2_min + offset_vec, col)
        p_a2_max = curr.copy(); p_a2_max[a2] = max_pos[a2]
        self.line_renderer.add_line(curr + offset_vec, p_a2_max + offset_vec, col)
        scr_pos = self.project_point_to_screen(curr[0], curr[1], curr[2])
        if not scr_pos: return
        sx, sy = scr_pos
        d1_min = abs(curr[a1] - min_pos[a1])
        d1_max = abs(curr[a1] - max_pos[a1])
        d2_min = abs(curr[a2] - min_pos[a2])
        d2_max = abs(curr[a2] - max_pos[a2])
        layout = [
            (d1_min, -40, 0),  
            (d1_max, 40, 0),   
            (d2_min, 0, 20),   
            (d2_max, 0, -20)   
        ]
        for i, (val, ox, oy) in enumerate(layout):
            label = self.aux_labels[i]
            label.set_text(f"{val:.2f}")
            lx = sx + ox - (label.w // 2)
            ly = sy + oy - (label.h // 2)
            self.labels_to_draw_queue.append((label, lx, ly))
    def _collect_lights_optimized(self):
        lights = []
        px, py, pz = self.camera.pos
        radius = 2 
        cx, cy, cz = self.get_chunk_coords(px, pz, py)
        normals = [
            np.array([ 1.0,  0.0,  0.0], dtype=np.float32), 
            np.array([-1.0,  0.0,  0.0], dtype=np.float32), 
            np.array([ 0.0,  1.0,  0.0], dtype=np.float32), 
            np.array([ 0.0, -1.0,  0.0], dtype=np.float32), 
            np.array([ 0.0,  0.0,  1.0], dtype=np.float32), 
            np.array([ 0.0,  0.0, -1.0], dtype=np.float32)  
        ]
        cam_pos_np = self.camera.pos
        
        # 1. Статические огни (из чанков)
        for dx in range(-radius, radius + 1):
            for dy in range(-1, 2):
                for dz in range(-radius, radius + 1):
                    key = (cx + dx, cy + dy, cz + dz)
                    if key not in self.spatial_grid: continue
                    for ent in self.spatial_grid[key]:
                        # --- НОВОЕ: Пропускаем анимированные, их обработаем отдельно ---
                        if ent.is_animating: continue 
                        
                        if abs(ent.pos[0] - px) > 45 or abs(ent.pos[2] - pz) > 45:
                            continue
                        
                        # (Далее старый код сбора цвета...)
                        color_groups = {}
                        has_emission = False
                        for i in range(6):
                            col = ent.faces_colors[i]
                            if len(col) > 4 and col[4] > 0.05:
                                has_emission = True
                                rgb_key = (round(col[0], 2), round(col[1], 2), round(col[2], 2))
                                intensity = col[4]
                                if rgb_key not in color_groups:
                                    color_groups[rgb_key] = [[], 0.0]
                                color_groups[rgb_key][0].append(normals[i])
                                color_groups[rgb_key][1] += intensity
                        if not has_emission:
                            continue
                        for rgb, data in color_groups.items():
                            vec_list = data[0]
                            total_intensity = data[1]
                            count = len(vec_list)
                            avg_normal = np.sum(vec_list, axis=0)
                            norm_len = np.linalg.norm(avg_normal)
                            if norm_len > 0.001:
                                avg_normal /= norm_len 
                            offset_dist = max(ent.scale) * 0.6
                            light_pos = ent.pos + avg_normal * offset_dist
                            avg_int = total_intensity / count
                            final_intensity = avg_int * (1.0 + (count - 1) * 0.2)
                            dist_sq = np.sum((light_pos - cam_pos_np)**2)
                            lights.append((dist_sq, light_pos, rgb, final_intensity))

        # 2. Динамические огни (на анимированных дверях)
        for anim in self.door_animations:
            ent = anim['ent']
            # Рассчитываем матрицу поворота
            angle_deg = anim['current_angle']
            pivot = anim['pivot']
            axis_vec = anim['axis']
            
            rad = math.radians(angle_deg)
            c = math.cos(rad)
            s = math.sin(rad)
            ux, uy, uz = axis_vec
            rot_mat = np.array([
                [c + ux**2*(1-c),    ux*uy*(1-c) - uz*s, ux*uz*(1-c) + uy*s],
                [uy*ux*(1-c) + uz*s, c + uy**2*(1-c),    uy*uz*(1-c) - ux*s],
                [uz*ux*(1-c) - uy*s, uz*uy*(1-c) + ux*s, c + uz**2*(1-c)]
            ], dtype=np.float32)

            # Проверяем грани
            for i in range(6):
                col = ent.faces_colors[i]
                if len(col) > 4 and col[4] > 0.05:
                    intensity = col[4]
                    rgb = (col[0], col[1], col[2])
                    
                    # Берем базовую нормаль и вращаем её
                    base_normal = normals[i]
                    rotated_normal = np.dot(rot_mat, base_normal)
                    
                    # Рассчитываем позицию света:
                    # Берем "идеальный" центр двери, если бы она была в начале координат
                    # (Свет обычно исходит из центра грани)
                    # Сложнее: нам нужно повернуть смещение от пивота до центра грани
                    
                    # Центр энтити в текущем положении анимации рассчитывать сложно,
                    # проще взять original_pos и повернуть относительно pivot
                    
                    orig_pos = anim['original_pos']
                    
                    # Вектор от центра двери до центра грани (в исходном состоянии)
                    face_offset_local = base_normal * (ent.scale[i//2] * 0.5 + 0.1) # 0.1 - вынос света наружу
                    
                    # Центр грани в мировых (до поворота)
                    face_center_orig = orig_pos + face_offset_local
                    
                    # Поворачиваем точку face_center_orig вокруг pivot
                    vec = face_center_orig - pivot
                    rotated_vec = np.dot(rot_mat, vec)
                    final_light_pos = pivot + rotated_vec
                    
                    dist_sq = np.sum((final_light_pos - cam_pos_np)**2)
                    lights.append((dist_sq, final_light_pos, rgb, intensity))

        lights.sort(key=lambda x: x[0])
        return [(math.sqrt(l[0]), l[1], l[2], l[3]) for l in lights]
if __name__ == "__main__":
    app = App()
    app.run()
