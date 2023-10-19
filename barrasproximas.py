import model
import view
import controller

if __name__ == "__main__":
    model = model.Model()
    control = controller.Controller(model)
    app = view.App(controller=control)
    app.mainloop()
