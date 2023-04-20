using System.Diagnostics;
using System.Runtime.InteropServices;

namespace RucoyBot
{
    public partial class Form1 : Form
    {

        private const int WM_HOTKEY = 0x0312;
        private const int MOD_SHIFT = 0x0004;
        private const int VK_F5 = 0x74;
        [DllImport("user32.dll")]
        private static extern bool RegisterHotKey(IntPtr hWnd, int id, int fsModifiers, int vk);
        [DllImport("user32.dll")]
        private static extern bool UnregisterHotKey(IntPtr hWnd, int id);



        Process pybot = new Process();
        public bool isOn = false;


        public Form1()
        {
            InitializeComponent();
            RegisterHotKey(this.Handle, 1, MOD_SHIFT, VK_F5);
        }
        protected override void WndProc(ref Message m)
        {
            if (m.Msg == WM_HOTKEY && m.WParam.ToInt32() == 1)
            {
                // Handle the hotkey here
                button3.PerformClick();
            }
            base.WndProc(ref m);
            if (m.Msg == WM_NCHITTEST)
                m.Result = (IntPtr)(HT_CAPTION);
        }

        private const int WM_NCHITTEST = 0x84;
        private const int HT_CLIENT = 0x1;
        private const int HT_CAPTION = 0x2;

        private void button1_Click(object sender, EventArgs e)
        {
            Application.Exit();
        }


        string file = "main.py";
        string debug_mode = "False";
        string launch_type = "skilling";
        private List<string> target_list = new List<string>();
        
        private void button2_Click(object sender, EventArgs e)
        {
            string[] args = target_list.ToArray();
            if (isOn == false)
            {
                isOn = true;

                pybot.StartInfo.FileName = "Python";
                pybot.StartInfo.Arguments = $" \"{file}\" \"{debug_mode}\" \"{launch_type}\" \"{string.Join("//", args)}\"";
                pybot.StartInfo.UseShellExecute = false;
                if (debug_mode == "False") 
                {
                    pybot.StartInfo.CreateNoWindow = true;
                } 
                else
                {
                    pybot.StartInfo.CreateNoWindow = false;
                }
                pybot.Start();
                log("Starting");
            }
            else
            {
                return;
            }
        }
        private void log(string text)
        {
            DateTime currentTime = DateTime.Now;
            string time = currentTime.ToString("HH:mm:ss");
            richTextBox2.AppendText("[" + time + "]: " + text + "\n");
        }
        private void button3_Click(object sender, EventArgs e)
        {
            if (!isOn)
            {
                log("Attempted to stop the process without starting it");
            }
            if (isOn)
            {
                pybot.Kill();
                isOn = false;
                log("Stopping");
            }
        }

        private int hue = 0;
        private System.Windows.Forms.Timer rainbowTimer = new System.Windows.Forms.Timer();

        private void Form1_Load(object sender, EventArgs e)
        {
            rainbowTimer.Interval = 15; // change this to adjust the animation speed
            rainbowTimer.Tick += RainbowTimer_Tick;
            rainbowTimer.Start();
        }

        private void RainbowTimer_Tick(object sender, EventArgs e)
        {
            hue = (hue + 1) % 360; // increment the hue value
            Color color = ColorFromHSL(hue, 1, 0.5); // convert the hue to a color
            label2.ForeColor = color; // set the label's background color
        }

        private Color ColorFromHSL(int hue, double saturation, double lightness)
        {
            double chroma = (1 - Math.Abs(2 * lightness - 1)) * saturation;
            double huePrime = hue / 60.0;
            double x = chroma * (1 - Math.Abs(huePrime % 2 - 1));
            double r, g, b;
            if (huePrime < 1)
            {
                r = chroma;
                g = x;
                b = 0;
            }
            else if (huePrime < 2)
            {
                r = x;
                g = chroma;
                b = 0;
            }
            else if (huePrime < 3)
            {
                r = 0;
                g = chroma;
                b = x;
            }
            else if (huePrime < 4)
            {
                r = 0;
                g = x;
                b = chroma;
            }
            else if (huePrime < 5)
            {
                r = x;
                g = 0;
                b = chroma;
            }
            else
            {
                r = chroma;
                g = 0;
                b = x;
            }
            double m = lightness - chroma / 2.0;
            int red = (int)((r + m) * 255);
            int green = (int)((g + m) * 255);
            int blue = (int)((b + m) * 255);
            return Color.FromArgb(red, green, blue);
        }

        protected override void OnFormClosed(FormClosedEventArgs e)
        {
            UnregisterHotKey(this.Handle, 1);
            base.OnFormClosed(e);
        }

        private void richTextBox2_TextChanged(object sender, EventArgs e)
        {
            richTextBox2.SelectionStart = richTextBox2.Text.Length;
            richTextBox2.ScrollToCaret();
        }

        private void checkBox1_CheckedChanged(object sender, EventArgs e)
        {
            if(checkBox1.Checked == true)
            {
                debug_mode = "True";
            } 
            else if(checkBox1.Checked == false)
            {
                debug_mode = "False";
            }
        }

        private void label1_Click(object sender, EventArgs e)
        {

        }

        private void radioButton1_CheckedChanged(object sender, EventArgs e)
        {
            //skilling
            launch_type = "skilling";
        }

        private void radioButton2_CheckedChanged(object sender, EventArgs e)
        {
            //farming
            launch_type = "farming";
        }

        private void checkedListBox1_ItemCheck(object sender, ItemCheckEventArgs e)
        {
            string item = checkedListBox1.Items[e.Index].ToString();

            if (e.NewValue == CheckState.Checked)
            {
                target_list.Add(item);
            }
            else if (e.NewValue == CheckState.Unchecked)
            {
                target_list.Remove(item);
            }
        }
    }
}