# LLM commmand line tool helper

基于 LLM API 的命令行工具辅助工具。

## 设置

1. 将项目文件解压至文件夹中。
2. `pip install -r requirements.txt` 安装依赖。
3. 本项目使用智谱 AI 的**免费模型** GLM-4-flash，需要先在[智谱开放平台](https://open.bigmodel.cn/)注册账号并获取 API Key。
4. 修改`.env` 文件中的 `ZHIPU_API_KEY` 变量为你的 API Key。
5. 可以个性化配置想要使用的模型，参看智谱开放平台的[接口文档](https://open.bigmodel.cn/dev/api/normal-model/glm-4)中提供的模型编码。

## 使用

```shell
python main.py [-s] [-pe] [-l]
```

可选参数有：

- -s, --stream: 启用流式输出
- -pe, --prompt: 启用优化的 prompt
- -l, --log: 启用日志输出

程序使用过程中可以按下 `Ctrl+C` 退出，此外有可用的特殊命令：

- `/clear`: 清除对话上下文
- `/exit`: 退出程序

## 环境变量

将脚本目录添加到系统环境变量中，可以让用户在终端或命令提示符的任何地方直接运行 LLM 命令行工具。以下是具体步骤，适用于 **Windows** 和 **Unix 系统（Linux/macOS）**。

### **在 Windows 系统上**

#### 方法 1：通过系统设置添加环境变量

1. **打开系统设置**：

   - 右键点击“此电脑”或“计算机”，选择“属性”。
   - 点击“高级系统设置”。
   - 在弹出的窗口中，点击“环境变量”按钮。

2. **编辑系统环境变量 `Path`**：
   - 在“系统变量”部分，找到并选择 `Path`，然后点击“编辑”。
   - 点击“新建”，然后输入本项目目录路径（例如 `D:\path\to\llm-cli`）。
   - 点击“确定”保存。

#### 方法 2：通过命令行添加环境变量

1. **打开命令提示符**：

   - 按 `Win + R`，输入 `cmd`，然后按回车。

2. **临时添加环境变量**（仅对当前会话有效）：

   ```batch
   set PATH=%PATH%;C:\path\to\llm-cli
   ```

3. **永久添加环境变量**（需要管理员权限）：
   ```batch
   setx PATH "%PATH%;D:\path\to\llm-cli"
   ```

最后

### **在 Unix 系统上（Linux/macOS）**

#### 方法 1：通过编辑 shell 配置文件

1. **打开终端**。

2. **编辑 shell 配置文件**：

   - 根据你使用的 shell（如 `bash`、`zsh` 或 `fish`），编辑对应的配置文件：
     - 对于 `bash`，编辑 `~/.bashrc` 或 `~/.bash_profile`。
     - 对于 `zsh`，编辑 `~/.zshrc`。
     - 对于 `fish`，编辑 `~/.config/fish/config.fish`。

3. **添加项目根目录到 `PATH`**：

   - 在配置文件中添加以下内容：
     ```bash
     export PATH=$PATH:/path/to/llm-cli
     ```

4. **重新加载配置文件**：
   - 对于 `bash` 或 `zsh`：
     ```bash
     source ~/.bashrc  # 或者 source ~/.zshrc
     ```
   - 对于 `fish`：
     ```bash
     source ~/.config/fish/config.fish
     ```

### 方法 2：通过命令行临时添加环境变量

1. **打开终端**。

2. **临时添加环境变量**（仅对当前会话有效）：
   ```bash
   export PATH=$PATH:/path/to/llm-cli
   ```

### 方法 3：通过命令行永久添加环境变量

1. **打开终端**。

2. **永久添加环境变量**（需要管理员权限）：

   - 对于 `bash` 或 `zsh`：
     ```bash
     echo 'export PATH=$PATH:/path/to/llm-cli' | sudo tee -a /etc/profile
     ```
   - 对于 `fish`：
     ```bash
     echo 'set -gx PATH $PATH /path/to/llm-cli' | sudo tee -a /etc/fish/config.fish
     ```

3. **重新加载配置文件**：
   - 对于 `bash` 或 `zsh`：
     ```bash
     source /etc/profile
     ```
   - 对于 `fish`：
     ```bash
     source /etc/fish/config.fish
     ```
